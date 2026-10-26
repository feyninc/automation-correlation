"""Probe each model's reasoning ("thinking") behaviour on the route we will use: the default, and low / medium / high.

One short scheduling question per call; records whether the request was accepted, the reasoning and output tokens,
and the answer. Stdlib only (urllib, plus the AWS CLI for Bedrock).

    python3 -I scripts/probe_reasoning.py <project root>
"""
import csv, json, os, subprocess, sys, time, urllib.error, urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

root = Path(sys.argv[1])
CONF = Path("/home/user/.config/automation-correlation")
AZ = Path("/home/user/.azure-usefeyn")
PROMPT = ("Meetings today: A 9:00-10:30, B 10:15-11:00, C 10:45-12:00, D 12:30-13:15. Which pairs overlap, and what is the "
          "longest stretch with no meeting between 9:00 and 14:00? Answer in one line.")
LEVELS = [None, "low", "medium", "high"]

# (label, route, model id on that route, extra: provider tag for OpenRouter)
MODELS = [
    ("GPT-5.2", "openai", "gpt-5.2", None), ("GPT-5.4", "openai", "gpt-5.4", None), ("GPT-5.5", "openai", "gpt-5.5", None),
    ("GPT-5.6 Sol", "openai", "gpt-5.6-sol", None), ("GPT-6 Sol", "openai", "gpt-6-sol", None),
    ("GPT-6.1 Sol", "openai", "gpt-6.1-sol", None), ("GPT-6 Astra (judge)", "openai", "gpt-6-astra", None),
    ("Opus 4.5", "bedrock", "global.anthropic.claude-opus-4-5-20251101-v1:0", None),
    ("Opus 4.6", "bedrock", "global.anthropic.claude-opus-4-6-v1", None),
    ("Opus 4.7", "bedrock", "global.anthropic.claude-opus-4-7", None),
    ("Opus 4.8", "bedrock", "global.anthropic.claude-opus-4-8", None),
    ("Opus 5", "bedrock", "global.anthropic.claude-opus-5", None),
    ("Opus 5.5 (also judge)", "bedrock", "global.anthropic.claude-opus-5-5", None),
    ("DeepSeek V3.2", "azure", "deepseek-v3.2", None), ("DeepSeek V4 Flash", "azure", "deepseek-v4-flash", None),
    ("DeepSeek V4 Flash 0731", "azure", "deepseek-v4-flash-0731", None),
    ("DeepSeek V4.1 Flash (also judge)", "azure", "deepseek-v4.1-flash", None),
    ("Kimi K2.5", "azure", "kimi-k2.5", None), ("Kimi K2.6", "azure", "kimi-k2.6", None),
    ("Kimi K2 Thinking", "openrouter", "moonshotai/kimi-k2-thinking", "novita/bf16"),
    ("Kimi K3 (also judge)", "openrouter", "moonshotai/kimi-k3", "moonshotai/mxfp4"),
    ("Kimi K3.1 Pro", "openrouter", "moonshotai/kimi-k3.1-pro", "moonshotai/mxfp4"),
    ("DeepSeek V4.1 Flash 1017", "openrouter", "deepseek/deepseek-v4.1-flash-1017", "deepinfra/fp8"),
    ("GLM-4.7", "bedrock", "zai.glm-4.7", None), ("GLM-5", "bedrock", "zai.glm-5", None),
    ("GLM-5.1", "openrouter", "z-ai/glm-5.1", "z-ai/fp8"), ("GLM-5.2", "openrouter", "z-ai/glm-5.2", "z-ai/fp8"),
    ("GLM-5.3 (also judge)", "bedrock", "global.zai.glm-5.3", None),
    ("Gemini 4 Argon (judge)", "openrouter", "google/gemini-4-argon", "google-vertex/global"),
    ("Qwen3.8 Max Prime (judge)", "openrouter", "qwen/qwen3.8-max-prime", "alibaba"),
]


def post(url, headers, body, timeout=300):
    req = urllib.request.Request(url, json.dumps(body).encode(), {"Content-Type": "application/json", **headers})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.load(r), None
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code}: {e.read().decode(errors='replace')[:300]}"
    except Exception as e:  # noqa: BLE001 - recorded, not raised
        return None, f"{type(e).__name__}: {e}"[:300]


def chat(route, model, level, tag):
    msgs = [{"role": "user", "content": PROMPT}]
    if route == "openai":
        body = {"model": model, "messages": msgs, "max_completion_tokens": 16000}
        if level:
            body["reasoning_effort"] = level
        return post("https://api.openai.com/v1/chat/completions",
                    {"Authorization": "Bearer " + (CONF / "openai-key").read_text().strip()}, body)
    if route == "azure":
        body = {"model": model, "messages": msgs, "max_tokens": 16000}
        if level:
            body["reasoning_effort"] = level
        return post((CONF / "azure-endpoint").read_text().strip() + "/chat/completions",
                    {"api-key": (AZ / "foundry-key").read_text().strip()}, body)
    if route == "openrouter":
        body = {"model": model, "messages": msgs, "max_tokens": 16000,
                "provider": {"order": [tag], "allow_fallbacks": False}, "usage": {"include": True}}
        if level:
            body["reasoning"] = {"effort": level}
        return post("https://openrouter.ai/api/v1/chat/completions",
                    {"Authorization": "Bearer " + (CONF / "openrouter-key").read_text().strip()}, body)
    raise ValueError(route)


def bedrock(model, level):
    cmd = ["aws", "bedrock-runtime", "converse", "--model-id", model, "--output", "json",
           "--messages", json.dumps([{"role": "user", "content": [{"text": PROMPT}]}]),
           "--inference-config", json.dumps({"maxTokens": 16000})]
    if level and model.startswith(("zai.", "global.zai.")):  # GLM on Bedrock: OpenAI-style reasoning_effort
        cmd += ["--additional-model-request-fields", json.dumps({"reasoning_effort": level})]
    elif level and "opus-4-5" in model:  # no adaptive thinking on Opus 4.5; effort is a beta there
        cmd += ["--additional-model-request-fields",
                json.dumps({"anthropic_beta": ["effort-2025-11-24"], "output_config": {"effort": level},
                            "thinking": {"type": "enabled", "budget_tokens": 8000}})]
    elif level:
        cmd += ["--additional-model-request-fields",
                json.dumps({"thinking": {"type": "adaptive"}, "output_config": {"effort": level}})]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    if p.returncode:
        return None, (p.stderr.strip().splitlines() or ["error"])[-1][:300]
    return json.loads(p.stdout), None


def run(m, level):
    label, route, model, tag = m
    t = time.time()
    if route == "bedrock":
        d, err = bedrock(model, level)
    else:
        d, err = chat(route, model, level, tag)
    row = {"model": label, "route": route, "level": level or "default", "ok": err is None, "error": err or "",
           "reasoning_tokens": "", "output_tokens": "", "reasoning_visible_chars": "", "answer": "", "provider": "",
           "seconds": round(time.time() - t, 1)}
    if err:
        return row
    if route == "bedrock":
        blocks = d["output"]["message"]["content"]
        reasoning = "".join(b.get("reasoningContent", {}).get("reasoningText", {}).get("text", "") for b in blocks)
        row.update(output_tokens=d["usage"]["outputTokens"], reasoning_visible_chars=len(reasoning),
                   reasoning_tokens="present" if any("reasoningContent" in b for b in blocks) else 0,
                   answer=" ".join(b.get("text", "") for b in blocks if "text" in b)[:160])
    else:
        u = d.get("usage") or {}
        msg = d["choices"][0]["message"]
        reasoning = msg.get("reasoning_content") or msg.get("reasoning") or ""
        row.update(output_tokens=u.get("completion_tokens", ""),
                   reasoning_tokens=(u.get("completion_tokens_details") or {}).get("reasoning_tokens", ""),
                   reasoning_visible_chars=len(reasoning if isinstance(reasoning, str) else json.dumps(reasoning)),
                   answer=(msg.get("content") or "")[:160], provider=d.get("provider", ""))
    return row


only = sys.argv[2] if len(sys.argv) > 2 else ""  # optional: probe only models whose label contains this
jobs = [(m, lv) for m in MODELS if only in m[0] for lv in LEVELS]
with ThreadPoolExecutor(10) as ex:
    rows = list(ex.map(lambda j: run(*j), jobs))
out = root / ("data/reasoning-probe.csv" if not only else f"data/reasoning-probe-{only.lower().replace(' ', '-')}.csv")
with open(out, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)
for r in rows:
    print(f'{r["model"]:34s} {r["level"]:8s} {"ok " if r["ok"] else "ERR"} reason={r["reasoning_tokens"]!s:>7s} '
          f'out={r["output_tokens"]!s:>6s} vis={r["reasoning_visible_chars"]!s:>6s} {r["seconds"]:6.1f}s '
          f'{r["error"][:110] if r["error"] else r["answer"][:70]!r}')
