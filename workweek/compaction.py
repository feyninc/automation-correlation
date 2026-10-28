"""Compaction of the assistant's week-long conversation, after OpenCode's default
(packages/core/src/session/compaction.ts in anomalyco/opencode, read at 45b53fe6 on 2026-10-27).

The model writes its own summary, in a fixed template, of everything so far; the newest KEEP_TOKENS of the
conversation are kept word for word beside it. The request is the conversation unchanged plus the summary prompt, so
it reuses the prompt cache. Later requests open with one checkpoint message:

    <conversation-checkpoint><summary>S</summary><recent-context>tail</recent-context></conversation-checkpoint>

A later compaction updates the checkpoint rather than starting over. A reply that skips the template gets one
reminder. If the provider rejects the request as too long, it is resent as a text transcript with tool outputs cut.
The same procedure runs for every model; nothing native (OpenAI's encrypted compaction item is readable by OpenAI
models only). The engine compacts when the input reaches `compact_at` of the context window, and between days as
config `overnight` says: `compact` (this), `clear` (a fresh conversation) or `custom`, a function named in
`overnight_function` ("module:function") with the signature of `compact`: it gets the model, the conversation, the
tools and a list to append each call's usage to (not charged), and returns the conversation to continue with.
"""
from __future__ import annotations

import json

from inspect_ai.model import ChatMessage, ChatMessageAssistant, ChatMessageTool, ChatMessageUser, Model

KEEP_TOKENS = 15_000          # newest conversation kept word for word beside the summary (OpenCode's default)
CHARS_PER_TOKEN = 4           # until a call has been measured; the engine then passes the model's own ratio
TAIL_SHARE = 0.25             # the tail is at most this share of the compaction threshold (OpenCode's cap)
CLIP = 2_000                  # characters kept from each end of a long tool output in the transcript fallback
CHECKPOINT = "<conversation-checkpoint>"

TEMPLATE = """\
You MUST use this format for your response (you may omit sections that aren't applicable). Do not include the
<template> tags in your response.
<template>
## The worker's week
- [one or two sentences: who you assist, what this week is about for them]

## Open work
- [each item that still needs doing: what it is, who it is for, its deadline, its file under /world; or "(none)"]

## Proposals and promises
- [proposals you made that the worker has not acted on, and anything the worker or you promised someone, with times;
  or "(none)"]

## Decisions and rules
- [decisions already made and why; the policies, limits and approvals that govern the open work; or "(none)"]

## Facts and figures
- [exact amounts, counts, dates, names, identifiers and deadlines the open work turns on; or "(none)"]

## Done
- [work finished and how; or "(none)"]

## Next
1. [what you will do next, in order, or "(none)"]

## Relevant files
- `[path]`: [why it matters] (at most 15, most important first)
</template>"""

RULES = """\
Rules:
- Keep each section concise. Use terse, single-line bullets, not prose paragraphs or nested lists.
- Prefer short references over restating; leave out what you can find again under /world or in /home/assistant.
- Preserve exact file paths, names, amounts, dates, times, identifiers and quoted wording.
- Carry forward only requests and questions that are still open. Drop ones that newer history answered or resolved.
- Do not mention the summary process or that the conversation was compacted."""


def build_prompt(update: bool) -> str:
    shared = ["Summarize only what happened in the work and what you did. Leave out the instructions you were given at "
              "the start; you will receive them again.", TEMPLATE, RULES, "Do not continue the work or call tools.",
              "Return only the summary in the requested format, with no preamble or commentary."]
    if not update:
        return "\n\n".join(["You MUST summarize the conversation above into a structured summary that you will be "
                            "given to continue the work.", *shared])
    return "\n\n".join([
        "Update the existing checkpoint in the conversation above into one consolidated summary.",
        "Newer history always takes precedence over the existing checkpoint. Keep earlier information unless newer "
        "history contradicts, supersedes, resolves or makes it stale.",
        "Fold in newer work, decisions and facts. Move finished items from Open work to Done; drop answered questions "
        "and kept promises; keep what is still pending.",
        "Return only the updated Markdown sections, without the <conversation-checkpoint>, <summary> or "
        "<recent-context> tags.", *shared])


NUDGE = ("The previous response did not fill in the required summary template. Do not call tools. Return the summary as "
         "text using the exact section headings from the template.")
HEADINGS = [ln.strip() for ln in TEMPLATE.splitlines() if ln.startswith("## ")]


def as_text(m: ChatMessage, clip: int | None = None) -> str:
    """One message as transcript text; `clip` cuts long tool outputs to their head and tail."""
    if isinstance(m, ChatMessageTool):
        body = m.text
        if clip and len(body) > 2 * clip:
            body = body[:clip] + f"\n[... {len(body) - 2 * clip} characters cut ...]\n" + body[-clip:]
        return f"[tool result: {m.function}]\n{body}"
    if isinstance(m, ChatMessageAssistant):
        calls = "".join(f"\n[tool call: {c.function} {json.dumps(c.arguments, ensure_ascii=False)}]"
                        for c in m.tool_calls or [])
        return f"[assistant]\n{m.text}{calls}".rstrip()
    return f"[{m.role}]\n{m.text}"


def tail(messages: list[ChatMessage], keep: int = KEEP_TOKENS, chars_per_token: float = CHARS_PER_TOKEN) -> str:
    """The newest messages since the last checkpoint, as text, up to `keep` tokens; always at least the newest one."""
    out, size = [], 0
    for m in reversed(messages[1:]):
        if m.text.startswith(CHECKPOINT):
            break
        t = as_text(m)
        if out and size + len(t) > keep * chars_per_token:
            break
        out.append(t)
        size += len(t)
    return "\n\n".join(reversed(out))


def filled(text: str) -> bool:
    return any(ln.strip() in HEADINGS for ln in text.splitlines())


def too_long(error: BaseException) -> bool:
    s = str(error).lower()
    return any(x in s for x in ("context length", "context_length", "too long", "maximum context", "prompt is too long",
                                "input is too long", "reduce the length", "context window"))


async def compact(model: Model, messages: list[ChatMessage], tools: list, usage: list, keep: int = KEEP_TOKENS,
                  chars_per_token: float = CHARS_PER_TOKEN) -> list[ChatMessage]:
    """The conversation replaced by [system, checkpoint]; each call's usage is appended to `usage` (not charged).
    `keep` and `chars_per_token` size the verbatim tail; the engine caps `keep` and measures the ratio."""
    update = len(messages) > 1 and messages[1].text.startswith(CHECKPOINT)
    prompt = build_prompt(update)
    keep = tail(messages, keep, chars_per_token)

    async def ask(request: list[ChatMessage]) -> str:
        out = await model.generate(request, tools=tools)
        usage.append(out.usage.model_dump() if out.usage else {})
        if filled(out.completion):
            return out.completion
        out = await model.generate(request + [ChatMessageUser(content=NUDGE)], tools=tools)
        usage.append(out.usage.model_dump() if out.usage else {})
        return out.completion

    try:   # the conversation as sent, so the cached prefix is reused
        summary = await ask(messages + [ChatMessageUser(content=prompt)])
    except Exception as e:
        if not too_long(e):
            raise
        transcript = "\n\n".join(as_text(m, clip=CLIP) for m in messages[1:])
        summary = await ask([messages[0], ChatMessageUser(content=transcript + "\n\n" + prompt)])
    summary = summary.strip()
    checkpoint = (f"{CHECKPOINT}\n<summary>\n{summary}\n</summary>\n<recent-context>\n{keep}\n</recent-context>\n"
                  "</conversation-checkpoint>")
    return [messages[0], ChatMessageUser(content=checkpoint)]


def chars(messages: list[ChatMessage]) -> int:
    return sum(len(as_text(m)) for m in messages)


def estimate(messages: list[ChatMessage], chars_per_token: float = CHARS_PER_TOKEN) -> int:
    """A token count of messages from their characters."""
    return int(chars(messages) / chars_per_token)


def clear(messages: list[ChatMessage]) -> list[ChatMessage]:
    """A fresh conversation: the system prompt only."""
    return messages[:1]


def load(path: str):
    """The function named "module:function"."""
    import importlib
    module, _, name = path.partition(":")
    return getattr(importlib.import_module(module), name)
