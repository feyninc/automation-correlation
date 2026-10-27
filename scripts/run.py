"""Run the workweek benchmark for some models, professions and a time window, then print what happened.

    uv run python scripts/run.py --models all --professions all --start "D1 09:00" --end "D1 09:10" --log-dir logs/sample

--models and --professions take "all" or comma-separated names (model names from config/run.yaml; profession folder
names under professions/). Grade the logs afterwards with `python -m workweek.grade <log-dir>`.
"""
import argparse

from inspect_ai import eval as inspect_eval
from inspect_ai.model import GenerateConfig, get_model

from workweek import config, creds, providers  # noqa: F401
from workweek.engine import ROOT, workweek


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", default="all")
    ap.add_argument("--professions", default="all")
    ap.add_argument("--start", default="D1 00:00")
    ap.add_argument("--end", default="D5 23:59")
    ap.add_argument("--log-dir", default="logs/run")
    ap.add_argument("--max-samples", type=int, default=6)
    ap.add_argument("--max-models", type=int, default=8, help="models evaluated in parallel")
    a = ap.parse_args()
    creds.load()
    cfg = config.load(ROOT / "config/run.yaml")
    missing = cfg.missing_credentials()
    if missing:
        raise SystemExit(f"missing credentials: {missing}")
    names = None if a.models == "all" else set(a.models.split(","))
    specs = [m for m in cfg.models if names is None or m.name in names]
    if names and len(specs) != len(names):
        raise SystemExit(f"unknown models: {names - {m.name for m in specs}}")
    models = [get_model(m.model, config=GenerateConfig(**cfg.generate_for(m)), **m.model_args) for m in specs]
    logs = inspect_eval(workweek(professions=a.professions, start=a.start, end=a.end), model=models,
                        log_dir=a.log_dir, max_samples=a.max_samples, max_tasks=a.max_models, display="none",
                        fail_on_error=False, retry_on_error=2)
    for spec, log in zip(specs, logs):
        print(f"{spec.name}: {log.status}" + (f" ({log.error.message[:200]})" if log.error else ""))
        for s in log.samples or []:
            md = s.metadata
            print(f"  {s.id}: ticks {md.get('ticks')}, proposals {len(md.get('proposals', []))}, "
                  f"questions {len(md.get('questions', []))}" + (f", error {s.error.message[:120]}" if s.error else ""))


if __name__ == "__main__":
    main()
