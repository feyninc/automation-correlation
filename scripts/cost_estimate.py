"""Expected inference spend for the benchmark: tested models, the judge panel, episode generation.

Prices are per route in ROUTE below (2026-10-25). Token volumes come from the harness assumptions in SCENARIOS; every one is a guess until the
pilot measures it, which is why there are three.

    python3 -I scripts/cost_estimate.py <project root>
"""
import csv, json, sys
from pathlib import Path

root = Path(sys.argv[1])
EP = root / "data/openrouter/endpoints-2026-10-25"

# Route per model (owner, 10-25): GPT on OpenAI's API, Claude on Bedrock, DeepSeek and Kimi on Azure Foundry where
# Azure has them, everything else on OpenRouter. Prices in USD per million tokens: (bill to, route, input, output,
# cache read, cache write or None when writes cost nothing extra).
# Sources: OpenAI and Bedrock rows are those providers' endpoints in data/openrouter/endpoints-2026-10-25/;
# Kimi on Azure from the Azure retail prices API (global meters, 2026-10-25); DeepSeek on Azure is approximate
# (V4 Flash from OpenRouter's Azure endpoint, the rest at DeepSeek's list prices; the Azure meters were not found);
# OpenRouter rows from the chosen endpoint there.
ROUTE = {
    "openai/gpt-5.2": ("OpenAI", "openai", 1.75, 14, 0.175, None),
    "openai/gpt-5.4": ("OpenAI", "openai", 2.5, 15, 0.25, None),
    "openai/gpt-5.5": ("OpenAI", "openai", 5, 30, 0.5, None),
    "openai/gpt-5.6-sol": ("OpenAI", "openai", 4, 20, 0.4, None),
    "openai/gpt-6-sol": ("OpenAI", "openai", 2, 10, 0.2, None),
    "openai/gpt-6.1-sol": ("OpenAI", "openai", 2, 10, 0.1, None),
    "openai/gpt-6-astra": ("OpenAI", "openai", 10, 50, 1.0, None),
    "anthropic/claude-opus-4.5": ("Bedrock", "global.anthropic.claude-opus-4-5", 5, 25, 0.5, 6.25),
    "anthropic/claude-opus-4.6": ("Bedrock", "global.anthropic.claude-opus-4-6", 5, 25, 0.5, 6.25),
    "anthropic/claude-opus-4.7": ("Bedrock", "global.anthropic.claude-opus-4-7", 5, 25, 0.5, 6.25),
    "anthropic/claude-opus-4.8": ("Bedrock", "global.anthropic.claude-opus-4-8", 5, 25, 0.5, 6.25),
    "anthropic/claude-opus-5": ("Bedrock", "global.anthropic.claude-opus-5", 5, 25, 0.5, 6.25),
    "anthropic/claude-opus-5.5": ("Bedrock", "global.anthropic.claude-opus-5-5", 4, 20, 0.2, 5),
    "moonshotai/kimi-k2.5": ("Azure", "kimi-k2.5", 0.60, 3.00, 0.10, None),
    "moonshotai/kimi-k2.6": ("Azure", "kimi-k2.6", 0.95, 4.00, 0.16, None),
    "deepseek/deepseek-v3.2": ("Azure", "deepseek-v3.2 (approx.)", 0.58, 1.68, 0.058, None),
    "deepseek/deepseek-v4-flash": ("Azure", "deepseek-v4-flash", 0.21, 0.56, 0.031, None),
    "deepseek/deepseek-v4-flash-0731": ("Azure", "deepseek-v4-flash-0731 (approx.)", 0.21, 0.56, 0.031, None),
    "deepseek/deepseek-v4.1-flash": ("Azure", "deepseek-v4.1-flash (approx.)", 0.30, 1.20, 0.03, None),
    "moonshotai/kimi-k2-thinking": ("OpenRouter", "Novita bf16", 0.60, 2.50, 0.15, None),
    "moonshotai/kimi-k3": ("OpenRouter", "Moonshot AI", 3, 15, 0.3, None),
    "moonshotai/kimi-k3.1-pro": ("OpenRouter", "Moonshot AI", 2, 10, 0.2, None),
    # DeepSeek's own endpoint is blocked by the account's data policy (it trains on paid traffic): DeepInfra fp8.
    "deepseek/deepseek-v4.1-flash-1017": ("OpenRouter", "DeepInfra fp8", 0.098, 0.294, 0.00294, None),
    # GLM (added 2026-10-26): 4.7 and 5 on Bedrock (no prompt caching there: cache read 0 = every token at full price;
    # GLM-4.7's Bedrock price assumed equal to Z.ai's), 5.1 to 5.3 on Z.ai's own fp8 endpoint (GLM-5.3 is not
    # available to this AWS account on Bedrock).
    "z-ai/glm-4.7": ("Bedrock", "zai.glm-4.7 (price approx.)", 0.60, 2.20, 0, None),
    "z-ai/glm-5": ("Bedrock", "zai.glm-5", 1.00, 3.20, 0, None),
    "z-ai/glm-5.1": ("OpenRouter", "Z.AI fp8", 1.40, 4.40, 0.26, None),
    "z-ai/glm-5.2": ("OpenRouter", "Z.AI fp8", 1.40, 4.40, 0.26, None),
    "z-ai/glm-5.3": ("OpenRouter", "Z.AI fp8", 1.40, 4.40, 0.26, None),
    "google/gemini-4-argon": ("OpenRouter", "Google Vertex", 2, 10, 0.1, None),
    "qwen/qwen3.8-max-prime": ("OpenRouter", "Alibaba", 4, 12, 0.5, None),
}
JUDGES = ["anthropic/claude-opus-5.5", "openai/gpt-6-astra", "google/gemini-4-argon", "moonshotai/kimi-k3",
          "deepseek/deepseek-v4.1-flash", "qwen/qwen3.8-max-prime", "z-ai/glm-5.3"]
# Judging is offline, so OpenAI's Batch API and Bedrock batch inference (both half price) apply to those two judges.
BATCH = {"openai/gpt-6-astra": 0.5, "anthropic/claude-opus-5.5": 0.5}

OCCUPATIONS, SEEDS = 11, 3
DAYS, ACTIONS_PER_DAY = 5, 12

SCENARIOS = {
    #            calls/turn  base ctx  growth/call  output/call  proposals/episode  judge in  judge out
    "low":  dict(calls=2, base=6_000, grow=900, out=400, proposals=15, j_in=4_000, j_out=500),
    "mid":  dict(calls=3, base=8_000, grow=1_300, out=1_000, proposals=30, j_in=5_000, j_out=1_000),
    "high": dict(calls=5, base=10_000, grow=1_800, out=2_500, proposals=60, j_in=7_000, j_out=2_000),
}
OVERHEAD = 0.25  # pilots, reruns, debugging


def price(mid):
    bill, route, pin, pout, pcr, pcw = ROUTE[mid]
    p = {"prompt": pin / 1e6, "completion": pout / 1e6, "input_cache_read": pcr / 1e6,
         "input_cache_write": (pcw or 0) / 1e6}
    return bill, route, p


def episode_tokens(sc):
    """One context per day (reset each morning; the evening turn writes the notes carried over)."""
    turns = ACTIONS_PER_DAY + 1
    fresh = cached = 0
    out = 0
    for _ in range(DAYS):
        ctx_prev = 0
        for i in range(turns * sc["calls"]):
            ctx = sc["base"] + sc["grow"] * i
            cached += ctx_prev
            fresh += ctx - ctx_prev
            ctx_prev = ctx
            out += sc["out"]
    return fresh, cached, out


def model_cost(mid, fresh, cached, out):
    _, _, p = price(mid)
    if p["input_cache_read"] == 0:  # no caching on this endpoint: every input token at full price
        return (fresh + cached) * p["prompt"] + out * p["completion"]
    write = p["input_cache_write"] or p["prompt"]
    return fresh * write + cached * p["input_cache_read"] + out * p["completion"]


models = [r["openrouter_id"] for r in csv.DictReader(open(root / "data/models.csv"))]
rows, totals = [], {}
for name, sc in SCENARIOS.items():
    fresh, cached, out = episode_tokens(sc)
    runs = OCCUPATIONS * SEEDS
    tested = {m: model_cost(m, fresh, cached, out) * runs for m in models}
    proposals = sc["proposals"] * runs * len(models)
    judge = {j: proposals * BATCH.get(j, 1) * (sc["j_in"] * price(j)[2]["prompt"] + sc["j_out"] * price(j)[2]["completion"])
             for j in JUDGES}
    gen = OCCUPATIONS * (1_000_000 * price("anthropic/claude-opus-5.5")[2]["prompt"]
                         + 200_000 * price("anthropic/claude-opus-5.5")[2]["completion"])
    sub = sum(tested.values()) + sum(judge.values()) + gen
    totals[name] = dict(tested=sum(tested.values()), judges=sum(judge.values()), generation=gen,
                        overhead=sub * OVERHEAD, total=sub * (1 + OVERHEAD),
                        episode_in=fresh + cached, episode_out=out, proposals=proposals)
    for m, c in tested.items():
        rows.append([name, "tested", m, *price(m)[:2], round(c, 2)])
    for j, c in judge.items():
        rows.append([name, "judge", j, *price(j)[:2], round(c, 2)])

with open(root / "data/cost-estimate.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["scenario", "role", "model", "provider", "endpoint", "usd"])
    w.writerows(rows)

for name, t in totals.items():
    print(f"{name:5s} episode {t['episode_in'] / 1e6:5.2f}M in / {t['episode_out'] / 1e3:4.0f}k out | "
          f"tested ${t['tested']:8,.0f}  judges ${t['judges']:7,.0f}  generation ${t['generation']:4,.0f}  "
          f"overhead ${t['overhead']:6,.0f}  total ${t['total']:8,.0f}")
mid = [r for r in rows if r[0] == "mid"]
by_provider = {}
for r in mid:
    by_provider[r[3]] = by_provider.get(r[3], 0) + r[5]
gen = totals["mid"]["generation"]
by_provider["Bedrock"] = by_provider.get("Bedrock", 0) + gen
print("mid by bill-to, with the 25% overhead:", {k: round(v * (1 + OVERHEAD)) for k, v in sorted(by_provider.items(), key=lambda kv: -kv[1])})
for name in SCENARIOS:
    bp = {}
    for r in rows:
        if r[0] == name:
            bp[r[3]] = bp.get(r[3], 0) + r[5]
    bp["Bedrock"] = bp.get("Bedrock", 0) + totals[name]["generation"]
    print(f"  {name}:", {k: round(v * (1 + OVERHEAD)) for k, v in sorted(bp.items(), key=lambda kv: -kv[1])})
for r in mid:
    print(f"  {r[1]:6s} {r[2]:36s} {r[3]:15s} {r[4]:26s} ${r[5]:9,.2f}")
