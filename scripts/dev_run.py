import sys
from inspect_ai import eval as inspect_eval
from inspect_ai.model import get_model, GenerateConfig
from workweek import config, creds, providers  # noqa
from workweek.engine import workweek
creds.load()
cfg = config.load()
names = sys.argv[1].split(",")
models = [get_model(m.model, config=GenerateConfig(**cfg.generate_for(m)), **m.model_args) for m in cfg.models if m.name in names]
logs = inspect_eval(workweek(professions=sys.argv[2], start=sys.argv[3], end=sys.argv[4]), model=models, log_dir="logs/dev",
                    max_samples=4, display="none")
for l in logs:
    s = l.samples[0] if l.samples else None
    print(l.eval.model, l.status, (l.error.message[:300] if l.error else ""))
    if s:
        print("  ticks", s.metadata.get("ticks"), "proposals", len(s.metadata.get("proposals", [])), "questions", len(s.metadata.get("questions", [])))
        for p in s.metadata.get("proposals", [])[:6]:
            print("   ", p["t"], p["action"], p["target"][:60], "|", p["drafts"][0].get("text", "")[:100].replace("\n", " "))
        for q in s.metadata.get("questions", []):
            print("   Q", q["question"][:100], "-> A", q["answer"][:150])
