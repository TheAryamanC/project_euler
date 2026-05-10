import logging
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Callable, Optional

from openai import OpenAI, RateLimitError

from .config import (
    LLM_PROVIDER,
    DEEPSEEK_API_KEY, DEEPSEEK_MODEL,
    GROQ_API_KEY, GROQ_MODEL,
    OPENAI_API_KEY, OPENAI_MODEL,
    REPO_ROOT, SOLUTION_TIMEOUT,
)

logger = logging.getLogger(__name__)


def _make_client() -> tuple[OpenAI, str]:
    """Return (openai-compatible client, model name) for the configured provider."""
    if LLM_PROVIDER == "deepseek":
        if not DEEPSEEK_API_KEY:
            raise RuntimeError(
                "LLM_PROVIDER=deepseek but DEEPSEEK_API_KEY is not set. "
                "Get a free key at https://platform.deepseek.com"
            )
        return (
            OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com"),
            DEEPSEEK_MODEL,
        )
    if LLM_PROVIDER == "groq":
        if not GROQ_API_KEY:
            raise RuntimeError(
                "LLM_PROVIDER=groq but GROQ_API_KEY is not set. "
                "Get a free key at https://console.groq.com/keys"
            )
        return (
            OpenAI(api_key=GROQ_API_KEY, base_url="https://api.groq.com/openai/v1"),
            GROQ_MODEL,
        )
    # default: openai
    if not OPENAI_API_KEY:
        raise RuntimeError(
            "LLM_PROVIDER=openai but OPENAI_API_KEY is not set."
        )
    return OpenAI(api_key=OPENAI_API_KEY), OPENAI_MODEL


_client, _model = _make_client()

_MAX_RATE_LIMIT_RETRIES = 5  # inner retries purely for 429s; don't count as wrong-answer attempts


def _call_llm(messages: list[dict]) -> str:
    for rl_attempt in range(1, _MAX_RATE_LIMIT_RETRIES + 1):
        try:
            raw_resp = _client.chat.completions.with_raw_response.create(
                model=_model,
                messages=messages,
                temperature=0.2,
            )
            # Log remaining quota so we can spot if we're approaching limits
            rem_req = raw_resp.headers.get("x-ratelimit-remaining-requests", "?")
            rem_tok = raw_resp.headers.get("x-ratelimit-remaining-tokens", "?")
            logger.info(
                "Groq quota: %s requests remaining today, %s tokens remaining this minute",
                rem_req,
                rem_tok,
            )
            if rem_req not in ("?", None) and int(rem_req) <= 5:
                logger.warning("Daily request quota is nearly exhausted (%s left)!", rem_req)
            return raw_resp.parse().choices[0].message.content or ""
        except RateLimitError as exc:
            retry_after = 60
            try:
                retry_after = int(exc.response.headers.get("retry-after", 60))
            except Exception:
                pass
            logger.warning(
                "Rate limited (429) – waiting %ds before retry %d/%d",
                retry_after,
                rl_attempt,
                _MAX_RATE_LIMIT_RETRIES,
            )
            time.sleep(retry_after + 1)
    raise RuntimeError(
        f"LLM rate-limit retries exhausted after {_MAX_RATE_LIMIT_RETRIES} attempts."
    )


_STYLE_EXAMPLE = '''\
"""
Project Euler - Problem 22: Names Scores

Using names.txt, a 46K text file containing over five-thousand first names,
begin by sorting it into alphabetical order. Then working out the alphabetical
value for each name, multiply this value by its alphabetical position in the
list to obtain a name score.

For example, when the list is sorted into alphabetical order, COLIN, which is
worth 3 + 15 + 12 + 9 + 14 = 53, is the 938th name in the list. So, COLIN
would obtain a score of 938 x 53 = 49714.

What is the total of all the name scores in the file?
"""

def solution():
    with open("additional_files/names.txt") as f:
        names = f.read().replace(\'"\', \'\').split(\',\')
    names.sort()
    total = 0
    for i, name in enumerate(names, 1):
        name_value = sum(ord(c) - ord(\'A\') + 1 for c in name)
        total += i * name_value
    return total

if __name__ == "__main__":
    print(solution())  # Answer: 871198282
'''

_SYSTEM_PROMPT = f"""\
You are an expert competitive programmer specialising in Project Euler problems.

Your job is to produce a single, complete, correct Python 3 solution file.

STRICT FORMAT RULES
───────────────────
1. The file MUST start with a triple-quoted module docstring containing:
   • First line: "Project Euler - Problem <N>: <Title>"
   • Blank line
   • The full problem description (copy it verbatim)
2. Allowed imports: standard library only, plus sympy, numpy, scipy.
3. Define a function `solution()` that returns the final answer as a plain
   integer or string (no units, no formatting, no print inside it).
4. End the file with exactly these two lines:
       if __name__ == "__main__":
           print(solution())  # Answer: <the numeric answer>

STYLE EXAMPLE
─────────────
{_STYLE_EXAMPLE}

OUTPUT
──────
Respond with ONLY the raw Python source code - no markdown fences,
no explanations, no commentary outside the module docstring.
"""


def _list_additional_files() -> list[str]:
    d = REPO_ROOT / "additional_files"
    if not d.is_dir():
        return []
    return sorted(f"additional_files/{p.name}" for p in d.iterdir() if p.is_file())


def _build_user_message(problem: dict, previous_error: Optional[str]) -> str:
    lines = [
        f"Solve Project Euler Problem {problem['number']}: {problem['title']}",
        "",
        "PROBLEM DESCRIPTION",
        "-------------------",
        problem["text"],
        "",
    ]

    extra_files = _list_additional_files()
    if extra_files:
        lines += [
            "AVAILABLE INPUT FILES (paths relative to the repo root / CWD)",
            "--------------------------------------------------------------",
            *extra_files,
            "",
            "If the problem requires a file, open it with a path relative to the "
            "current working directory (e.g. open('additional_files/names.txt')).",
            "",
        ]

    if previous_error:
        lines += [
            "YOUR PREVIOUS ATTEMPT FAILED",
            "-----------------------------",
            previous_error,
            "",
            "Please diagnose the error and provide a fully corrected solution.",
        ]

    return "\n".join(lines)


def _strip_fences(text: str) -> str:
    """Remove markdown code fences and <think> reasoning blocks."""
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()
    match = re.search(r"```(?:python)?\n(.*?)```", text, re.DOTALL)
    return match.group(1).strip() if match else text.strip()


def _run_code(code: str, problem_number: int) -> tuple[Optional[str], Optional[str]]:
    """Write code to a temp file, execute it, return (stdout, error_msg)"""
    tmp = REPO_ROOT / f"_tmp_p{problem_number:03d}.py"
    try:
        tmp.write_text(code, encoding="utf-8")
        result = subprocess.run(
            [sys.executable, str(tmp)],
            capture_output=True,
            text=True,
            timeout=SOLUTION_TIMEOUT,
            cwd=str(REPO_ROOT),
        )
        if result.returncode != 0:
            err = (result.stderr or "").strip() or f"Exit code {result.returncode}"
            return None, err
        output = result.stdout.strip()
        if not output:
            return None, "Solution produced no output"
        return output, None
    except subprocess.TimeoutExpired:
        return None, f"Timed out after {SOLUTION_TIMEOUT}s"
    finally:
        tmp.unlink(missing_ok=True)



def generate_solution(problem: dict, max_retries: int = 3, answer_validator: Optional[Callable[[str], bool]] = None,) -> tuple[str, str]:
    """Generate and validate a Python solution for the problem"""
    messages: list[dict] = [{"role": "system", "content": _SYSTEM_PROMPT}]
    previous_error: Optional[str] = None

    for attempt in range(1, max_retries + 1):
        logger.info(
            "LLM attempt %d/%d for problem %d",
            attempt,
            max_retries,
            problem["number"],
        )

        user_msg = _build_user_message(problem, previous_error)
        messages.append({"role": "user", "content": user_msg})

        raw_code = _call_llm(messages)
        code = _strip_fences(raw_code)
        # Keep the code in conversation history so follow-up retries have context
        messages.append({"role": "assistant", "content": code})

        answer, run_error = _run_code(code, problem["number"])

        if run_error:
            logger.warning("Attempt %d – runtime error: %s", attempt, run_error)
            previous_error = f"Runtime / execution error:\n{run_error}"
            continue

        logger.info("Attempt %d – solution output: %s", attempt, answer)

        if answer_validator is None:
            return code, answer  # no validation requested

        if answer_validator(answer):
            logger.info("Answer accepted by validator on attempt %d", attempt)
            return code, answer

        logger.warning(
            "Attempt %d – answer '%s' rejected by validator", attempt, answer
        )
        previous_error = (
            f"The answer you produced ('{answer}') was submitted to Project Euler "
            f"and marked INCORRECT. Re-read the problem carefully and try again."
        )

    raise RuntimeError(
        f"Could not solve problem {problem['number']} correctly "
        f"after {max_retries} attempt(s)."
    )