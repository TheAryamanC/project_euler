import logging
import subprocess
from pathlib import Path

from .config import REPO_ROOT, GIT_AUTHOR_NAME, GIT_AUTHOR_EMAIL

logger = logging.getLogger(__name__)


def _git(*args: str, check: bool = True) -> subprocess.CompletedProcess:
    """Run a git sub-command in the repo root"""
    return subprocess.run(
        ["git", *args],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        check=check,
    )


def ensure_git_identity() -> None:
    """Set user.name / user.email in the local git config if not already set"""
    for key, value in (("user.name", GIT_AUTHOR_NAME), ("user.email", GIT_AUTHOR_EMAIL),):
        result = _git("config", "--get", key, check=False)
        if result.returncode != 0 or not result.stdout.strip():
            _git("config", key, value)
            logger.debug("Set git config %s = %s", key, value)


def commit_and_push(
    file_path: Path,
    problem_number: int,
    answer: str,
    extra_files: list[Path] | None = None,
    state_file: Path | None = None,
) -> None:
    """Stage file(s), commit, and push"""
    ensure_git_identity()

    relative = file_path.relative_to(REPO_ROOT)
    _git("add", str(relative))

    for extra in extra_files or []:
        if extra.exists():
            _git("add", str(extra.relative_to(REPO_ROOT)))

    if state_file and state_file.exists():
        _git("add", str(state_file.relative_to(REPO_ROOT)))

    commit_msg = (
        f"solve: Problem {problem_number:03d}\n\n"
        f"Answer: {answer}\n"
        f"[automated - daily ML workflow]"
    )
    _git("commit", "-m", commit_msg)
    logger.info("Committed %s", relative)

    # Pull with rebase so we stay in sync with any concurrent remote changes
    rebase = _git("pull", "--rebase", "origin", "master", check=False)
    if rebase.returncode != 0:
        logger.warning(
            "git pull --rebase failed:\n%s\nAttempting push anyway.",
            rebase.stderr,
        )

    _git("push", "origin", "master")
    logger.info("Pushed to origin/master")