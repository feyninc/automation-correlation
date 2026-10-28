"""Run the workweek benchmark for some models, professions and a time window, then print what happened.

    uv run python scripts/run.py --models run --professions all --start "D1 09:00" --end "D1 09:10" --log-dir logs/sample

--models takes "run" (the default: each lab's newest model on or before each `run.snapshots` date, and its latest; 20
models), "all" (every model in config/run.yaml) or comma-separated names. --professions takes "all" or profession
folder names under professions/. The full run goes in batches of three professions, so each batch's cost is known before
the next starts; the run prints what each sample cost. Grade the logs afterwards with `python -m workweek.grade`.
"""
import argparse

from inspect_ai import eval as inspect_eval
from inspect_ai.model import GenerateConfig, get_model

from workweek import config, creds, providers  # noqa: F401
from workweek.engine import ROOT, workweek


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", default="run")
    ap.add_argument("--professions", default="all")
    ap.add_argument("--start", default="D1 00:00")
    ap.add_argument("--end", default="D5 23:59")
    ap.add_argument("--log-dir", default="logs/run")
    ap.add_argument("--config", default="config/run.yaml", help="the run's config, relative to the repository")
    ap.add_argument("--seeds", type=int, default=0, help="runs of each week (0: the config's run.seeds)")
    ap.add_argument("--max-samples", type=int, default=0, help="professions run at once per model (0: all of them)")
    ap.add_argument("--max-models", type=int, default=0, help="models run at once (0: all of them)")
    ap.add_argument("--max-sandboxes", type=int, default=48,
                    help="Docker sandboxes at once; about 30 MB each, so 48 leaves room on a 4 GB machine")
    a = ap.parse_args()
    creds.load()
    cfg = config.load(ROOT / a.config)
    seeds = a.seeds or cfg.run.seeds
    missing = cfg.missing_credentials()
    if missing:
        raise SystemExit(f"missing credentials: {missing}")
    names = None if a.models in ("all", "run") else set(a.models.split(","))
    specs = cfg.run_models() if a.models == "run" else [m for m in cfg.models if names is None or m.name in names]
    if names and len(specs) != len(names):
        raise SystemExit(f"unknown models: {names - {m.name for m in specs}}")
    models = [get_model(m.model, config=GenerateConfig(**cfg.generate_for(m)), **cfg.model_args_for(m)) for m in specs]
    n_prof = len(list((ROOT / "professions").glob("*/episode"))) if a.professions == "all" else len(a.professions.split(","))
    logs = inspect_eval(workweek(professions=a.professions, start=a.start, end=a.end, run_path=a.config, epochs=seeds),
                        model=models, log_dir=a.log_dir, max_samples=a.max_samples or n_prof * seeds, max_tasks=a.max_models or len(models), max_sandboxes=a.max_sandboxes, display="none",
                        fail_on_error=False, retry_on_error=2)
    spent = dict.fromkeys(config.BILLED, 0.0)
    total = worker = 0.0
    for spec, log in zip(specs, logs):
        print(f"{spec.name}: {log.status}" + (f" ({log.error.message[:200]})" if log.error else ""))
        for s in log.samples or []:
            md = s.metadata
            usage = {k: config.add_usage(u.model_dump(), md.get("prior_usage", {}).get(k)) for k, u in (s.model_usage or {}).items()}
            compacting = md.get("compaction_usage", {}).get(spec.model)       # the harness's, not charged
            cost = (spec.price.cost(config.net_usage(usage[spec.model], compacting), md.get("long_context_usage"))
                    if spec.model in usage else 0.0)
            sim = sum(cfg.user_model.price.cost(u) for k, u in usage.items() if k == cfg.user_model.model)
            total, worker = total + cost, worker + sim
            spent[config.billing(spec.model)] += cost
            spent[config.billing(cfg.user_model.model)] += sim
            print(f"  {s.id}: ticks {md.get('ticks')}, proposals {len(md.get('proposals', []))}, "
                  f"questions {len(md.get('questions', []))}, compactions {md.get('compactions', 0)}, ${cost:.2f}"
                  + (f", error {s.error.message[:120]}" if s.error else ""))
    print(f"cost: tested models ${total:.2f}, simulated worker ${worker:.2f} (judging is priced by workweek.grade)")
    print("  by billing: " + ", ".join(f"{b} ${v:.2f}" for b, v in spent.items()))


if __name__ == "__main__":
    main()
