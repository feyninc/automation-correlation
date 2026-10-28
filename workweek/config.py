"""The run config (config/run.yaml): tested models, judges, the simulated worker, run settings; with checks."""
from __future__ import annotations

import datetime as dt
import os
from pathlib import Path
from typing import Any, Literal

import yaml
from pydantic import BaseModel, Field, model_validator

KNOWN_FAMILIES = {"openai", "anthropic", "moonshot", "deepseek", "zai", "google", "alibaba"}
PROVIDER_CREDENTIALS = {          # model-string prefix -> environment variable it needs
    "openai": "OPENAI_API_KEY",
    "openrouter": "OPENROUTER_API_KEY",
    "openai-api/azure": "AZURE_API_KEY",
    "bedrock": "AWS_BEARER_TOKEN_BEDROCK",
}
BILLING = {                        # model-string prefix -> who pays; OpenRouter is the only route paid in cash
    "bedrock": "Bedrock credits",
    "openai-api/azure": "Azure credits",
    "openai": "OpenAI credits",
}
BILLED = ("Bedrock credits", "Azure credits", "OpenAI credits", "OpenRouter")


def net_usage(usage: dict, less: dict | None) -> dict:
    """An Inspect ModelUsage dump minus another (compaction's tokens are the harness's, not the model's)."""
    return {k: v - (less or {}).get(k, 0) if isinstance(v, (int, float)) else v for k, v in usage.items()}


def billing(model: str) -> str:
    return next((b for p, b in BILLING.items() if model.startswith(p + "/")), "OpenRouter")


class Price(BaseModel):
    input: float
    output: float
    cache_read: float = 0.0
    cache_write: float | None = None
    long_above: int | None = None      # a call whose prompt exceeds this many tokens is priced at the multipliers below
    long_input_x: float = 1.0          # on input, cache reads and cache writes
    long_output_x: float = 1.0

    def cost(self, usage: dict, long: dict | None = None) -> float:
        """USD for an Inspect ModelUsage dump; its input_tokens already exclude cache reads and writes. `long` is the
        part of `usage` from calls over `long_above`, which pays the long-context surcharge on top."""
        extra = 0.0
        if long:
            base = self.cost(long)
            out = long.get("output_tokens", 0) * self.output / 1e6
            extra = (base - out) * (self.long_input_x - 1) + out * (self.long_output_x - 1)
        write = self.input if self.cache_write is None else self.cache_write
        return extra + (usage.get("input_tokens", 0) * self.input + usage.get("output_tokens", 0) * self.output
                + (usage.get("input_tokens_cache_read") or 0) * self.cache_read
                + (usage.get("input_tokens_cache_write") or 0) * write) / 1e6


class ModelSpec(BaseModel):
    name: str
    model: str                         # passed to Inspect unchanged
    family: str
    released: dt.date | None = None
    generate: dict[str, Any] = {}       # Inspect GenerateConfig fields (reasoning_effort, ...)
    model_args: dict[str, Any] = {}     # provider routing etc.
    price: Price | None = None
    context_window: int | None = None  # tokens, the largest variant on this route; compaction starts at run.compact_at of it
    compact_tokens: int | None = None  # compact at this many tokens instead, when lower (below a long-context price break)


class JudgeSpec(ModelSpec):
    weight: float
    report_with_dropout: bool = True


class RunSettings(BaseModel):
    cadence_minutes: float = 5
    speed_file: str = ""                # p50 time to first token and throughput per model (offline timing)
    seeds: int = 3
    max_tool_calls_per_tick: int = 25
    max_output_tokens_per_call: int = 16000
    compact_at: float = 0.8             # share of a model's context window at which its conversation is compacted
    overnight: Literal["compact", "clear", "custom"] = "compact"   # what happens to the conversation between days
    overnight_function: str = ""        # "module:function" for overnight: custom; see workweek/compaction.py
    snapshots: list[dt.date] = []       # the run takes each lab's newest model on or before each date, and its latest
    send_arm: bool = False
    professions: list[str] | str = "all"
    eci_factor: dict[str, Any] = {"value": 1.0, "source": ""}


class RunConfig(BaseModel):
    run: RunSettings
    user_model: ModelSpec
    defaults: dict[str, Any] = {}
    models: list[ModelSpec]
    judges: list[JudgeSpec]

    @model_validator(mode="after")
    def _checks(self):
        errs = []
        names = [m.name for m in self.models]
        if len(set(names)) != len(names):
            errs.append("duplicate model names")
        for m in [*self.models, *self.judges, self.user_model]:
            if "/" not in m.model:
                errs.append(f"{m.name}: model string {m.model!r} has no provider prefix")
            if m.family not in KNOWN_FAMILIES:
                errs.append(f"{m.name}: unknown family {m.family!r}")
        for m in self.models:
            if m.released is None:
                errs.append(f"{m.name}: released missing")
            if m.price is None:
                errs.append(f"{m.name}: price missing")
            if not m.context_window:
                errs.append(f"{m.name}: context_window missing")
        total = sum(j.weight for j in self.judges)
        if abs(total - 1) > 1e-4:
            errs.append(f"judge weights sum to {total:.6f}, not 1")
        if any(j.weight < 0 for j in self.judges):
            errs.append("negative judge weight")
        if len({j.family for j in self.judges}) != len(self.judges):
            errs.append("two judges share a family (leave-own-family-out would drop both)")
        for fam in {m.family for m in self.models}:
            left = sum(j.weight for j in self.judges if not (j.report_with_dropout and j.family == fam))
            if left <= 0:
                errs.append(f"dropping family {fam} leaves no judge weight")
        if self.run.overnight == "custom" and ":" not in self.run.overnight_function:
            errs.append("overnight: custom needs overnight_function as 'module:function'")
        if self.run.overnight != "custom" and self.run.overnight_function:
            errs.append("overnight_function is set but overnight is not custom")
        if not 0 < self.run.compact_at <= 1:
            errs.append("compact_at must be a share of the context window, in (0, 1]")
        if self.run.cadence_minutes <= 0:
            errs.append("cadence_minutes must be positive")
        if errs:
            raise ValueError("config errors:\n  " + "\n  ".join(errs))
        return self

    def run_models(self) -> list[ModelSpec]:
        """For each lab: its newest model released on or before each snapshot date, and its latest; oldest first."""
        out: dict[str, ModelSpec] = {}
        for fam in sorted({m.family for m in self.models}):
            line = sorted((m for m in self.models if m.family == fam), key=lambda m: m.released)
            for d in self.run.snapshots:
                before = [m for m in line if m.released <= d]
                if before:
                    out[before[-1].name] = before[-1]
            out[line[-1].name] = line[-1]
        return sorted(out.values(), key=lambda m: (m.released, m.name))

    def spec(self, model: str) -> ModelSpec:
        return next(m for m in self.models if m.model == model)

    def generate_for(self, m: ModelSpec) -> dict[str, Any]:
        return {**self.defaults.get("generate", {}), **m.generate,
                "max_tokens": self.run.max_output_tokens_per_call}

    def missing_credentials(self) -> list[str]:
        out = []
        for m in [*self.models, *self.judges, self.user_model]:
            for prefix, var in PROVIDER_CREDENTIALS.items():
                if m.model.startswith(prefix + "/") and not os.environ.get(var):
                    out.append(f"{m.name}: {var} not set")
        return sorted(set(out))


def load(path: str | Path = "config/run.yaml") -> RunConfig:
    return RunConfig.model_validate(yaml.safe_load(Path(path).read_text()))
