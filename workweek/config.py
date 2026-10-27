"""The run config (config/run.yaml): tested models, judges, the simulated worker, run settings; with checks."""
from __future__ import annotations

import datetime as dt
import os
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field, model_validator

KNOWN_FAMILIES = {"openai", "anthropic", "moonshot", "deepseek", "zai", "google", "alibaba"}
PROVIDER_CREDENTIALS = {          # model-string prefix -> environment variable it needs
    "openai": "OPENAI_API_KEY",
    "openrouter": "OPENROUTER_API_KEY",
    "openai-api/azure": "AZURE_API_KEY",
    "bedrock": "AWS_BEARER_TOKEN_BEDROCK",
}


class Price(BaseModel):
    input: float
    output: float
    cache_read: float = 0.0
    cache_write: float | None = None

    def cost(self, usage: dict) -> float:
        """USD for an Inspect ModelUsage dump; its input_tokens already exclude cache reads and writes."""
        write = self.input if self.cache_write is None else self.cache_write
        return (usage.get("input_tokens", 0) * self.input + usage.get("output_tokens", 0) * self.output
                + (usage.get("input_tokens_cache_read") or 0) * self.cache_read
                + (usage.get("input_tokens_cache_write") or 0) * write) / 1e6


class Speed(BaseModel):
    ttft_p50_s: float | None = None
    throughput_tps: float | None = None


class ModelSpec(BaseModel):
    name: str
    model: str                         # passed to Inspect unchanged
    family: str
    released: dt.date | None = None
    generate: dict[str, Any] = {}       # Inspect GenerateConfig fields (reasoning_effort, ...)
    model_args: dict[str, Any] = {}     # provider routing etc.
    price: Price | None = None
    speed: Speed = Speed()


class JudgeSpec(ModelSpec):
    weight: float
    report_with_dropout: bool = True


class RunSettings(BaseModel):
    cadence_minutes: float = 5
    seeds: int = 3
    max_tool_calls_per_tick: int = 25
    max_output_tokens_per_call: int = 16000
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
            if m.price is None:
                errs.append(f"{m.name}: price missing")
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
        if self.run.cadence_minutes <= 0:
            errs.append("cadence_minutes must be positive")
        if errs:
            raise ValueError("config errors:\n  " + "\n  ".join(errs))
        return self

    def generate_for(self, m: ModelSpec) -> dict[str, Any]:
        return {**self.defaults.get("generate", {}), **m.generate,
                "max_tokens": self.run.max_output_tokens_per_call}

    def missing_speed(self) -> list[str]:
        return [m.name for m in self.models if m.speed.ttft_p50_s is None or m.speed.throughput_tps is None]

    def missing_credentials(self) -> list[str]:
        out = []
        for m in [*self.models, *self.judges, self.user_model]:
            for prefix, var in PROVIDER_CREDENTIALS.items():
                if m.model.startswith(prefix + "/") and not os.environ.get(var):
                    out.append(f"{m.name}: {var} not set")
        return sorted(set(out))


def load(path: str | Path = "config/run.yaml") -> RunConfig:
    return RunConfig.model_validate(yaml.safe_load(Path(path).read_text()))
