import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

REPO_ROOT: Path = Path(__file__).parent.parent.resolve()

OPENAI_API_KEY: str = os.environ["OPENAI_API_KEY"]
PE_USERNAME: str = os.environ["PE_USERNAME"]
PE_PASSWORD: str = os.environ["PE_PASSWORD"]

PE_COOKIE_FILE: Path = REPO_ROOT / os.environ.get("PE_COOKIE_FILE", "automation/cookies.json")

OPENAI_MODEL: str = os.environ.get("OPENAI_MODEL", "gpt-4o")
MAX_RETRIES: int = int(os.environ.get("MAX_RETRIES", "3"))
SOLUTION_TIMEOUT: int = int(os.environ.get("SOLUTION_TIMEOUT", "120"))  # seconds

GIT_PUSH: bool = os.environ.get("GIT_PUSH", "true").lower() == "true"

GIT_AUTHOR_NAME: str = os.environ.get("GIT_AUTHOR_NAME", "project-euler-bot")
GIT_AUTHOR_EMAIL: str = os.environ.get("GIT_AUTHOR_EMAIL", "project-euler-bot@users.noreply.github.com")