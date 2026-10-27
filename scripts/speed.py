"""Snapshot each model's speed on the provider it runs on, from OpenRouter's endpoint stats (last 30 minutes).

    uv run python scripts/speed.py                      # writes data/openrouter/speed-snapshot-<date>.csv

A cross-check only: the grader's timing uses the week averages in `run.speed_file` (config/run.yaml).

For every tested model, judge and the simulated worker: p50/p90 latency to first token (seconds) and p50/p90
throughput (output tokens a second) of the OpenRouter endpoint that matches its route (OpenAI for GPT, Amazon
Bedrock for Bedrock, Azure for Azure where listed, else the lab's own endpoint; the pinned provider for OpenRouter
routes).
"""
import csv
import datetime as dt
import json
import statistics
import urllib.request

from workweek import config, creds
from workweek.engine import ROOT

LAB_PROVIDER = {"deepseek": "DeepSeek", "moonshotai": "Moonshot AI", "z-ai": "Z.AI", "anthropic": "Anthropic"}


def openrouter_id(model: str) -> str:
    """bedrock/global.anthropic.claude-opus-4-8 -> anthropic/claude-opus-4.8, openai-api/azure/kimi-k2.5 -> ..."""
    route, _, name = model.partition("/")
    if route == "openrouter":
        return name
    if route == "openai":
        return model
    if route == "bedrock":
        name = name.split(".", 1)[1] if name.startswith("global.") else name
        lab, _, m = name.partition(".")
        m = m.split("-v1")[0].split("-2025")[0]
        m = __import__("re").sub(r"(\d)-(\d)", r"\1.\2", m)
        return f"{'z-ai' if lab == 'zai' else lab}/{m}"
    if route == "openai-api":
        m = name.split("/", 1)[1]
        return f"{'moonshotai' if m.startswith('kimi') else 'deepseek'}/{m}"
    raise ValueError(model)


def wanted(spec) -> tuple[str, str | None]:
    """(provider name, tag prefix) of the endpoint matching the route."""
    route = spec.model.split("/")[0]
    if route == "openrouter":
        order = (spec.model_args.get("provider") or {}).get("order") or []
        return "", order[0] if order else None
    if route == "openai":
        return "OpenAI", None
    if route == "bedrock":
        return "Amazon Bedrock", None
    return "Azure", None


def fetch(oid: str, key: str) -> list[dict]:
    req = urllib.request.Request(f"https://openrouter.ai/api/v1/models/{oid}/endpoints",
                                 headers={"Authorization": f"Bearer {key}"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r).get("data", {}).get("endpoints", [])


def main():
    creds.load()
    cfg = config.load(ROOT / "config/run.yaml")
    key = (__import__("pathlib").Path.home() / ".config/automation-correlation/openrouter-key").read_text().strip()
    rows = []
    specs = [("tested", m) for m in cfg.models] + [("judge", j) for j in cfg.judges] + [("worker", cfg.user_model)]
    for role, spec in specs:
        oid = openrouter_id(spec.model)
        eps = [e for e in fetch(oid, key) if e.get("latency_last_30m") and e.get("throughput_last_30m")]
        name, tag = wanted(spec)
        pick = [e for e in eps if (tag and str(e.get("tag", "")).startswith(tag)) or (name and e["provider_name"] == name)]
        pick = [e for e in pick if e.get("service_tier") in (None, "default", "standard")] or pick
        if not pick and name == "Azure":
            lab = LAB_PROVIDER.get(oid.split("/")[0])
            pick = [e for e in eps if e["provider_name"] == lab]
        basis = "route" if pick else "median of all providers"
        if pick:
            e = pick[0]
            lat, thr, prov = e["latency_last_30m"], e["throughput_last_30m"], e["provider_name"]
        elif eps:
            lat = {k: statistics.median(x["latency_last_30m"][k] for x in eps) for k in ("p50", "p90")}
            thr = {k: statistics.median(x["throughput_last_30m"][k] for x in eps) for k in ("p50", "p90")}
            prov = f"{len(eps)} providers"
        else:
            rows.append({"role": role, "name": spec.name, "openrouter_id": oid, "basis": "no stats"})
            continue
        rows.append({"role": role, "name": spec.name, "openrouter_id": oid, "provider": prov, "basis": basis,
                     "ttft_p50_s": round(lat["p50"] / 1000, 3), "ttft_p90_s": round(lat["p90"] / 1000, 3),
                     "tps_p50": round(thr["p50"], 1), "tps_p90": round(thr["p90"], 1)})
    out = ROOT / f"data/openrouter/speed-snapshot-{dt.date.today().isoformat()}.csv"
    fields = ["role", "name", "openrouter_id", "provider", "basis", "ttft_p50_s", "ttft_p90_s", "tps_p50", "tps_p90"]
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    for r in rows:
        print(r)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
