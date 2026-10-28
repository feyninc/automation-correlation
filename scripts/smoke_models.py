"""Smoke test every model in config/run.yaml through Inspect: one tool call, the tool result, a final answer,
with the configured reasoning settings; records token usage per route.

    uv run python scripts/smoke_models.py [name-filter]
"""
import asyncio
import csv
import sys
import time

from inspect_ai.model import ChatMessageSystem, ChatMessageTool, ChatMessageUser, GenerateConfig, get_model
from inspect_ai.tool import ToolInfo, ToolParam, ToolParams

from workweek import config, creds

creds.load()
cfg = config.load()
only = sys.argv[1] if len(sys.argv) > 1 else ""

ADD = ToolInfo(name="add", description="Add two integers.",
               parameters=ToolParams(properties={"a": ToolParam(type="integer"), "b": ToolParam(type="integer")},
                                     required=["a", "b"]))


async def one(spec):
    t0 = time.time()
    row = {"name": spec.name, "model": spec.model, "tool_call": False, "final": "", "input": 0, "output": 0,
           "reasoning": "", "cache_read": "", "error": ""}
    try:
        model = get_model(spec.model, config=GenerateConfig(**cfg.generate_for(spec)), **cfg.model_args_for(spec))
        msgs = [ChatMessageSystem(content="You are a careful assistant. Use tools when asked."),
                ChatMessageUser(content="Use the add tool to add 2 and 3, then tell me the result in one word.")]
        out = await model.generate(msgs, tools=[ADD])
        usage = [out.usage]
        calls = out.message.tool_calls or []
        row["tool_call"] = bool(calls)
        if calls:
            msgs.append(out.message)
            for c in calls:
                msgs.append(ChatMessageTool(content=str(int(c.arguments.get("a", 0)) + int(c.arguments.get("b", 0))),
                                            tool_call_id=c.id, function=c.function))
            out2 = await model.generate(msgs, tools=[ADD])
            usage.append(out2.usage)
            row["final"] = (out2.completion or "").strip()[:40]
        u = [x for x in usage if x]
        row["input"] = sum(x.input_tokens for x in u)
        row["output"] = sum(x.output_tokens for x in u)
        row["reasoning"] = sum((x.reasoning_tokens or 0) for x in u) if any(x.reasoning_tokens for x in u) else ""
        row["cache_read"] = sum((x.input_tokens_cache_read or 0) for x in u) if any(x.input_tokens_cache_read for x in u) else ""
    except Exception as e:  # noqa: BLE001
        row["error"] = f"{type(e).__name__}: {e}"[:300]
    row["seconds"] = round(time.time() - t0, 1)
    return row


async def main():
    specs = [m for m in [*cfg.models, *cfg.judges, cfg.user_model] if only.lower() in m.name.lower()]
    seen, uniq = set(), []
    for s in specs:
        if (s.model, s.name) not in seen:
            seen.add((s.model, s.name))
            uniq.append(s)
    rows = await asyncio.gather(*(one(s) for s in uniq))
    with open("data/smoke-models.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    for r in rows:
        print(f"{r['name']:28s} tool={'Y' if r['tool_call'] else 'n'} final={r['final']!r:12s} in={r['input']:>6} "
              f"out={r['output']:>6} reason={r['reasoning']!s:>6} {r['seconds']:5.1f}s {r['error'][:120]}")


asyncio.run(main())
