#!/usr/bin/env python3
"""Daily orchestrator - get project, solve, and commit"""

import json
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from automation.config import GIT_PUSH, MAX_RETRIES, PE_SUBMIT, REPO_ROOT
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

    # Establishing a projecteuler.net session is OPTIONAL. It is only needed to
    # submit answers back to PE for profile credit, and PE gates its sign-in
    # behind a CAPTCHA on purpose — so a human must have exported a session
    # cookie beforehand (python -m automation.export_cookies). The core job —
    # fetch today's public problem, solve it, and commit to GitHub — needs no
    # login at all, so we never abort just because there's no session.
    can_submit = PE_SUBMIT and pe.ensure_session()

    number = _read_next_problem()
    logger.info("Targeting problem %d", number)

    problem = pe.get_problem(number)
    logger.info("Fetched: %s", problem["title"])
    if problem["downloaded_files"]:
        logger.info("Downloaded supplemental files: %s", problem["downloaded_files"])

    if can_submit:
        def validator(answer: str) -> bool:
            return pe.submit_answer(number, answer)
    else:
        logger.info(
            "No Project Euler submission this run — the solution will be verified "
            "by executing it locally, then committed to the repository."
        )
        validator = None

    try:
        code, answer = generate_solution(
            problem,
            max_retries=MAX_RETRIES,
            answer_validator=validator,
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
        commit_and_push(dest, number, answer, extra_files=extra_files)
    else:
        logger.info("GIT_PUSH is disabled; skipping commit/push.")

    verified = "verified by Project Euler" if can_submit else "self-verified locally"
    logger.info(
        "Problem %d solved (%s) and committed. Answer: %s",
        number,
        verified,
        answer,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())