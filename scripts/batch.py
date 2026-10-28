"""Run a batch of professions, one `scripts/run.py` process per profession (all run models in each), with live control.

    uv run python scripts/batch.py --professions claims-adjusters,accountants,customer-service-representatives \
        --log-dir logs/batch-1 --parallel 2

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
    a = ap.parse_args()
    log_dir = (ROOT / a.log_dir).resolve()
    log_dir.mkdir(parents=True, exist_ok=True)
    control = log_dir / "control.json"
    if not control.exists():
        control.write_text(json.dumps({"parallel": a.parallel}) + "\n")
    (log_dir / "DONE").unlink(missing_ok=True)
    queue = a.professions.split(",")
    running: dict[str, subprocess.Popen] = {}
    done: dict[str, int] = {}
    env = {**os.environ, "WORKWEEK_CONTROL": str(log_dir)}
    while queue or running:
        try:
            parallel = int(json.loads(control.read_text()).get("parallel", a.parallel))
        except (ValueError, OSError):
            parallel = a.parallel
        while queue and len(running) < parallel:
            p = queue.pop(0)
            out = open(log_dir / f"{p}.out", "w")
            running[p] = subprocess.Popen(
                [sys.executable, str(ROOT / "scripts/run.py"), "--models", a.models, "--professions", p,
                 "--start", a.start, "--end", a.end, "--log-dir", str(log_dir / p)],
                cwd=ROOT, env=env, stdout=out, stderr=subprocess.STDOUT)
        for p, proc in list(running.items()):
            if proc.poll() is not None:
                done[p] = proc.returncode
                del running[p]
        status = {"parallel": parallel, "paused": (log_dir / "PAUSE").exists(), "queued": queue,
                  "running": {p: proc.pid for p, proc in running.items()}, "finished": done,
                  "at": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())}
        (log_dir / "status.json").write_text(json.dumps(status, indent=1) + "\n")
        time.sleep(20)
    (log_dir / "DONE").write_text(json.dumps(done) + "\n")


if __name__ == "__main__":
    main()
