# Architecture (draft, 10-25)

One engine, many worlds. The code that runs an episode is the same for every occupation and every model; what
changes is data: the channel specs, the episode files and the judge rubrics. Nothing is generated as code.

```
channels/*.yaml ─┐
                 ├─> engine ──> trajectory.jsonl ──> grader ──> grades.jsonl ──> analysis
episodes/*.json ─┘     ^                               ^
                       │                               │
              model adapter                 checks (code) + judge (LLM)
        (one API, token + cost log)       rubrics: core + channel + occupation + need
```

## 1. Channel specs (`channels/<name>.yaml`)

A channel is a declarative tool: email, slack, docs, phone, tickets, repo. Each spec gives:

- `actions`: name, parameters (JSON Schema), and kind: `read` (list, open, search), `propose` (draft, reply,
  edit, say) or `act` (send; exposed only in the send arm, intercepted and logged, never delivered).
- `state`: the shape it keeps (threads, documents, a queue, a live call).
- `timing`: `async` (email, slack, docs) or `sync` (phone: a live call with a patience window per turn).
- `costs`: the economics. `do_minutes` (the human doing the action), `review_minutes` (the human reading a
  proposal), per action; occupations may override. These feed net time saved, so their sources are written down.

The engine turns the specs into one CLI the model drives through a single tool, `run("<command>")`, the same for
every model and provider (older models are weaker at native function calling; a text CLI is uniform).

## 2. Episodes (`episodes/<soc>-<n>.json`)

One file is one occupation's week. Validated by `schema/episode.schema.json`.

- `world`: the worker's role, organization, contacts, documents on Monday morning.
- `days[]`: per day, `arrivals` (timestamped items on any channel; 8 AM batch plus the day's later ones),
  `human_actions` (the scripted human, ~12 a day; each is a decision point), `calls` (phone: caller turns with the
  human's scripted replies and each turn's patience).
- `needs[]`: planted work. `id`, the O*NET task id it comes from, trigger, deadline, a `check` (a small predicate
  over proposals: channel, recipient, document, before time T, mentions X), a rubric, and minutes it saves.
- `traps[]`: things to leave alone (phishing, FYI-only, someone else's message, a decision only the human makes,
  pressure to send). A `check` that fires when a proposal touches them.

The world never reacts to the model: the human, callers and arrivals follow the script, and the model's
proposals sit in a pending list it can see (so it does not repeat itself).

## 3. Engine

- Simulated clock and event queue. Loop: apply arrivals up to the next human action, show it to the model, let it
  act (read freely, propose or `wait`) within a step budget, log, advance. 5 PM: the "prepare for tomorrow" turn.
- Time is simulated, never wall-clock (wall-clock measures the provider's servers, not the model). Each command
  costs simulated seconds; on a call, the model's output costs speaking time and each turn must land inside the
  caller's patience window or it is recorded as late. Open: whether hidden reasoning tokens are charged (they
  should be on the phone; decide once, for every model).
- Deterministic given the episode and the model's outputs: replaying a trajectory reproduces the same state.

## 4. Model adapter

Python 3.12 throughout (engine, grader, analysis), managed with uv, `uv.lock` pinning every dependency by hash.

LiteLLM (`litellm.completion(model="openrouter/<provider>/<model>", ...)`) over OpenRouter, for the tested models
and the judges alike. Logs per call: model id, the OpenRouter provider that served it, input, cached, output and
reasoning tokens, and OpenRouter's reported cost when it returns one. Cost is also computed later from
`prices.yaml` (launch price and current price per model; OpenRouter's catalog gives only today's), so a price
correction never needs a rerun. Pin the provider per model where OpenRouter allows it, so one model is not
served by different hosts across runs.

What OpenRouter serves (10-25 catalog, 467 models): OpenAI from GPT-4 (2023) through GPT-6.1, every one with tool
support, the longest single-family series; Anthropic only from Claude Opus 4.1 (2025-08) on; Google Gemini from
2.5; Llama 3.1 to 4; DeepSeek from V3 (2024-12); Qwen, Mistral.

## 5. Grader (offline, rerunnable on stored trajectories)

1. Checks first: each need's and trap's predicate over the proposals gives recall, false positives and harm,
   with no LLM.
2. Judge for quality: accept as-is / accept with edits / reject, plus edit size. Its prompt is composed of layers,
   not written per combination:
   - core (fixed for everything: the three-way scale and its definitions, so the press-enter rate means the same
     in every occupation),
   - channel module (phone: timeliness, turn-taking; email: completeness; repo: tests pass),
   - occupation context (the role and its norms, from O*NET),
   - the need's own rubric and, where it exists, the human's reference version.
   A panel of six judges (owner, 10-25), one per family, given the same composed prompt, each pinned to a dated
   snapshot: Claude Opus 5.5, GPT-6 Astra, Gemini 4 Argon, Kimi K3, DeepSeek V4.1 Flash, Qwen's latest flagship.
   Gemini and Qwen are unaffiliated with any tested family. Kimi and DeepSeek may be partly distilled from Claude
   or GPT, so their votes may not be independent of those two.
   - Primary grade: the panel without the tested model's own family. Every tested family (Anthropic, OpenAI,
     Kimi, DeepSeek) has a judge, so that panel is always five, and its median on the ordered scale
     (reject < edit < accept) is never tied.
   - Secondary grade: all six, median with ties broken downward (an accept/edit tie is "edit"), reported beside it.
   - Agreement: among the judges (Krippendorff's alpha, and the full pairwise matrix) and each judge against the
     hand grades.
   - Bias, measured rather than assumed: self-preference (does a judge rate its own family's proposals higher than
     the other judges do?) and distillation-preference (do Kimi and DeepSeek rate Claude's and GPT's proposals higher
     than Gemini and Qwen do, and agree with Claude and GPT more than with each other?).
3. Objective checks wherever they exist (tests for code, a ledger that reconciles, a total that sums).
4. Hand-graded sample per occupation for judge agreement (Cohen's kappa).

## 6. Episode generator

LLM drafts an episode from the occupation's O*NET tasks, the channel specs and the schema; then:
validator (schema, every reference resolves, times consistent, every need reachable and tied to an O*NET task) →
`review` CLI where the owner accepts or fixes each need and trap → frozen and hashed. Trajectories record the hash.

## Harness checks (before any model run)

- Oracle agent (proposes exactly the scripted human's future actions): near-full recall, every check fires.
- No-op agent: zero proposals, zero recall, no errors.
- Random agent: the floor, and a check that traps fire.
