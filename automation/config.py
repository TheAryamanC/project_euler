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

# Credentials are optional: PE gates its sign-in behind a CAPTCHA, so this bot
# never logs in programmatically. They default to empty so the pipeline can run
# (solve + commit) with no Project Euler account at all.
PE_USERNAME: str = os.environ.get("PE_USERNAME", "")
PE_PASSWORD: str = os.environ.get("PE_PASSWORD", "")
PE_COOKIE_FILE: Path = REPO_ROOT / os.environ.get("PE_COOKIE_FILE", "automation/cookies.json")

# Submitting answers to projecteuler.net requires a human-established session
# cookie. When enabled but no valid session exists, submission is skipped and the
# solution is still solved and committed.
PE_SUBMIT: bool = os.environ.get("PE_SUBMIT", "true").lower() == "true"

MAX_RETRIES: int = int(os.environ.get("MAX_RETRIES", "3"))
SOLUTION_TIMEOUT: int = int(os.environ.get("SOLUTION_TIMEOUT", "120"))  # seconds

GIT_PUSH: bool = os.environ.get("GIT_PUSH", "true").lower() == "true"
GIT_AUTHOR_NAME: str = os.environ.get("GIT_AUTHOR_NAME", "project-euler-bot")
GIT_AUTHOR_EMAIL: str = os.environ.get("GIT_AUTHOR_EMAIL", "project-euler-bot@users.noreply.github.com")