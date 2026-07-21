#!/usr/bin/env python3
"""Daily orchestrator - get project, solve, and commit"""

import json
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from automation.config import GIT_PUSH, MAX_RETRIES, REPO_ROOT
from automation.euler_client import ProjectEulerClient
from automation.git_ops import commit_and_push
from automation.solver import generate_solution

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


_STATE_FILE = REPO_ROOT / "automation" / "state.json"


def _read_next_problem() -> int:
    """Return the next problem number to solve (1-indexed, starts at 1)."""
    if _STATE_FILE.exists():
        try:
            data = json.loads(_STATE_FILE.read_text(encoding="utf-8"))
            return int(data["next_problem"])
        except (KeyError, ValueError, json.JSONDecodeError):
            pass
    return 1


def _advance_state(current: int) -> None:
    """Persist the next problem number to solve."""
    _STATE_FILE.write_text(
        json.dumps({"next_problem": current + 1}, indent=2),
        encoding="utf-8",
    )


def _solution_path(number: int) -> Path:
    problems_dir = REPO_ROOT / "problems"
    problems_dir.mkdir(exist_ok=True)
    return problems_dir / f"problem{number:03d}.py"


def _embed_answer_comment(code: str, answer: str) -> str:
    """Ensure the __main__ block ends with  # Answer: <answer>."""
    marker = f"# Answer: {answer}"
    if marker in code:
        return code
    return code.replace("print(solution())", f"print(solution())  {marker}")


def main() -> int:
    pe = ProjectEulerClient()

    number = _read_next_problem()
    logger.info("Targeting problem %d", number)

    problem = pe.get_problem(number)
    logger.info("Fetched: %s", problem["title"])
    if problem["downloaded_files"]:
        logger.info("Downloaded supplemental files: %s", problem["downloaded_files"])

    try:
        code, answer = generate_solution(
            problem,
            max_retries=MAX_RETRIES,
        )
    except RuntimeError as exc:
        logger.error("Solver exhausted all retries: %s", exc)
        return 1

    code = _embed_answer_comment(code, answer)
    dest = _solution_path(number)
    dest.write_text(code, encoding="utf-8")
    logger.info("Saved %s", dest.name)

    _advance_state(number)

    if GIT_PUSH:
        extra_files = [REPO_ROOT / "additional_files" / f for f in problem["downloaded_files"]]
        commit_and_push(
            dest,
            number,
            answer,
            extra_files=extra_files,
            state_file=_STATE_FILE,
        )
    else:
        logger.info("GIT_PUSH is disabled; skipping commit/push.")

    logger.info("Problem %d solved and committed. Answer: %s", number, answer)
    return 0


if __name__ == "__main__":
    sys.exit(main())