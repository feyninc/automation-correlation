"""Run a batch of professions, one `scripts/run.py` process per profession (all run models in each), with live control.

    uv run python scripts/batch.py --professions claims-adjusters,accountants,customer-service-representatives \
        --log-dir logs/batch-1 --parallel 2

With --per-model, each (profession, model) week is a process of its own (logs in <log-dir>/<profession>/<model>/),
so a batch spreads over every core instead of one per profession; --parallel then counts those processes.

Control, live, in the log directory:
- `control.json` {"parallel": N}: how many profession processes run at once; raise it to start the next one.
- `PAUSE` (an empty file): every running week waits before its next tick; delete it to resume. The simulated clock
  stops too, so nothing in the week changes; a pause over about five minutes costs one cache rewrite per running week.
- `status.json`: written every 20 seconds: each profession's state, pid and log directory.
- `DONE`: written when every profession has finished; `python -m workweek.grade <log-dir> --watch` stops on it.
"""
import argparse
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--professions", required=True, help="comma-separated, run in this order")
    ap.add_argument("--log-dir", required=True)
    ap.add_argument("--parallel", type=int, default=2, help="profession processes at once (control.json overrides)")
    ap.add_argument("--models", default="run")
    ap.add_argument("--start", default="D1 00:00")
    ap.add_argument("--end", default="D5 23:59")
    ap.add_argument("--per-model", action="store_true", help="one process per profession and model")
    a = ap.parse_args()
    log_dir = (ROOT / a.log_dir).resolve()
    log_dir.mkdir(parents=True, exist_ok=True)
    control = log_dir / "control.json"
    if not control.exists():
        control.write_text(json.dumps({"parallel": a.parallel}) + "\n")
    (log_dir / "DONE").unlink(missing_ok=True)
    queue = [(p, None) for p in a.professions.split(",")]
    if a.per_model:
        sys.path.insert(0, str(ROOT))
        from workweek import config
        cfg = config.load(ROOT / "config/run.yaml")
        names = [m.name for m in cfg.run_models()] if a.models == "run" else a.models.split(",")
        queue = [(p, m) for p, _ in queue for m in names]
    running: dict[str, subprocess.Popen] = {}
    done: dict[str, int] = {}
    env = {**os.environ, "WORKWEEK_CONTROL": str(log_dir)}
    while queue or running:
        try:
            parallel = int(json.loads(control.read_text()).get("parallel", a.parallel))
        except (ValueError, OSError):
            parallel = a.parallel
        while queue and len(running) < parallel:
            p, m = queue.pop(0)
            key = p if m is None else f"{p}/{re.sub(r'[^\w.-]+', '_', m)}"
            (log_dir / key).mkdir(parents=True, exist_ok=True)
            out = open(log_dir / f"{key}.out", "w")
            running[key] = subprocess.Popen(
                [sys.executable, str(ROOT / "scripts/run.py"), "--models", m or a.models, "--professions", p,
                 "--start", a.start, "--end", a.end, "--log-dir", str(log_dir / key)],
                cwd=ROOT, env=env, stdout=out, stderr=subprocess.STDOUT)
        for p, proc in list(running.items()):
            if proc.poll() is not None:
                done[p] = proc.returncode
                del running[p]
        status = {"parallel": parallel, "paused": (log_dir / "PAUSE").exists(), "queued": [f"{p}/{m}" if m else p for p, m in queue],
                  "running": {p: proc.pid for p, proc in running.items()}, "finished": done,
                  "at": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())}
        (log_dir / "status.json").write_text(json.dumps(status, indent=1) + "\n")
        time.sleep(20)
    (log_dir / "DONE").write_text(json.dumps(done) + "\n")


if __name__ == "__main__":
    main()
