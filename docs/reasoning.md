# Reasoning settings (2026-10-26)

Every model runs at its lab's **medium** reasoning setting, set explicitly on every call (owner, 2026-10-26). Defaults
are never relied on: they differ by model and even by host (DeepSeek V4.1 Flash thinks by default on DeepInfra and
does not on Azure).

Evidence: `scripts/probe_reasoning.py` asked each model one short scheduling question on its own route, with no
setting and at low / medium / high (`data/reasoning-probe.csv`). One easy question shows whether thinking is on and
whether the setting is accepted; it does not measure how much a model thinks on real work (the pilot does).

| Model (route) | Default, observed | Medium is sent as |
| --- | --- | --- |
| GPT-5.2, GPT-5.4 (OpenAI) | no reasoning (0 tokens) | `reasoning_effort: "medium"` |
| GPT-5.5, 5.6 Sol, 6 Sol, 6.1 Sol (OpenAI) | reasoning; OpenAI's docs: default `medium` | same |
| GPT-6 Astra, judge (OpenAI) | reasoning; no `none` allowed | same |
| Opus 4.5 (Bedrock) | no thinking | `anthropic_beta: ["effort-2025-11-24"]`, `output_config.effort: "medium"`, `thinking: {type: enabled, budget_tokens: 8000}` (no adaptive thinking on 4.5) |
| Opus 4.6, 4.7, 4.8 (Bedrock) | no thinking | `thinking: {type: adaptive}`, `output_config.effort: "medium"` |
| Opus 5, Opus 5.5 (Bedrock; 5.5 also judge) | thinks (adaptive) | same |
| DeepSeek V3.2, V4 Flash, V4 Flash 0731, V4.1 Flash (Azure; V4.1 Flash also judge) | no thinking | `reasoning_effort: "medium"` (turns thinking on) |
| Kimi K2.5, K2.6 (Azure) | thinks | `reasoning_effort: "medium"` |
| Kimi K2 Thinking, K3, K3.1 Pro (OpenRouter; K3 also judge) | thinks | `reasoning: {effort: "medium"}` |
| DeepSeek V4.1 Flash 1017 (OpenRouter, DeepInfra fp8) | thinks | `reasoning: {effort: "medium"}` |
| GLM-4.7, GLM-5 (Bedrock) | no thinking at low or medium; thinks at high | `reasoning_effort: "high"` (GLM's thinking is on/off, and on Bedrock only `high` turns it on; see below) |
| GLM-5.1, 5.2, 5.3 (OpenRouter, Z.ai fp8; 5.3 also judge) | thinks | `reasoning: {effort: "medium"}` |
| Gemini 4 Argon, judge (OpenRouter, Google Vertex) | no thinking on the probe below high | `reasoning: {effort: "medium"}` |
| Qwen3.8 Max Prime, judge (OpenRouter, Alibaba) | thinks | `reasoning: {effort: "medium"}` |

Caveats for the paper:

- "Medium" is each lab's own word, not a common unit. Anthropic's effort default is high, so medium is a step below
  Anthropic's default but OpenAI's default for GPT-5.5 on.
- Adaptive thinking decides per call: at medium Opus 4.6 thought on the probe, Opus 4.7 did not at any level.
- GLM has no effort levels, only thinking on or off (Z.ai's API), so its "medium" is "thinking on". On Bedrock,
  `reasoning_effort` low and medium leave thinking off and high turns it on (`data/reasoning-probe-glm.csv`), and
  Z.ai's own `thinking: {type: enabled}` is ignored there; so GLM on Bedrock is sent `high`.
- DeepSeek documents low / high / max for V4; what Azure does with `medium` is not documented.
- Reasoning token counts are not comparable across routes: OpenAI and OpenRouter report them, Bedrock and Azure
  bill them inside output tokens without a separate count.
