"""Load API credentials from files outside the repository into the environment Inspect reads."""
import os
from pathlib import Path

CONF = Path.home() / ".config/automation-correlation"
AZURE_KEY = Path.home() / ".azure-usefeyn/foundry-key"


def load() -> None:
    def put(var: str, path: Path) -> None:
        if not os.environ.get(var) and path.exists():
            os.environ[var] = path.read_text().strip()

    put("OPENAI_API_KEY", CONF / "openai-key")
    put("OPENROUTER_API_KEY", CONF / "openrouter-key")
    put("AZURE_API_KEY", AZURE_KEY)                 # Inspect "openai-api/azure/<deployment>"
    put("AZURE_BASE_URL", CONF / "azure-endpoint")
    put("AWS_BEARER_TOKEN_BEDROCK", CONF / "bedrock-token")   # or from the environment, if set there
    os.environ.setdefault("AWS_REGION", "us-east-1")
    os.environ.setdefault("AWS_DEFAULT_REGION", os.environ["AWS_REGION"])   # the one botocore reads
