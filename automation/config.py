import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

REPO_ROOT: Path = Path(__file__).parent.parent.resolve()

LLM_PROVIDER: str = os.environ.get("LLM_PROVIDER", "deepseek").lower()

DEEPSEEK_API_KEY: str = os.environ.get("DEEPSEEK_API_KEY", "")
DEEPSEEK_MODEL: str = os.environ.get("DEEPSEEK_MODEL", "deepseek-reasoner")

GROQ_API_KEY: str = os.environ.get("GROQ_API_KEY", "")
GROQ_MODEL: str = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")

OPENAI_API_KEY: str = os.environ.get("OPENAI_API_KEY", "")
OPENAI_MODEL: str = os.environ.get("OPENAI_MODEL", "gpt-4o")

MAX_RETRIES: int = int(os.environ.get("MAX_RETRIES", "3"))
SOLUTION_TIMEOUT: int = int(os.environ.get("SOLUTION_TIMEOUT", "120"))  # seconds

GIT_PUSH: bool = os.environ.get("GIT_PUSH", "true").lower() == "true"
GIT_AUTHOR_NAME: str = os.environ.get("GIT_AUTHOR_NAME", "project-euler-bot")
GIT_AUTHOR_EMAIL: str = os.environ.get("GIT_AUTHOR_EMAIL", "project-euler-bot@users.noreply.github.com")