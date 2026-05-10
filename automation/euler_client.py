import json
import logging
from pathlib import Path
from typing import Optional
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

from .config import PE_USERNAME, PE_PASSWORD, PE_COOKIE_FILE, REPO_ROOT

_DATA_EXTENSIONS = {".txt", ".csv", ".dat", ".gz", ".zip", ".rtf"} # for supplemental files

logger = logging.getLogger(__name__)

_BASE = "https://projecteuler.net"
_LOGIN_URL = f"{_BASE}/sign_in"
_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}


class ProjectEulerClient:
    """Stateful HTTP client for projecteuler.net"""

    def __init__(self) -> None:
        self.session = requests.Session()
        self.session.headers.update(_HEADERS)
        self._logged_in = False
        self._load_cookies()

    def _load_cookies(self) -> None:
        """Populate the session from cookies.json if it exists"""
        if not PE_COOKIE_FILE or not PE_COOKIE_FILE.exists():
            return
        try:
            cookies = json.loads(PE_COOKIE_FILE.read_text(encoding="utf-8"))
            for c in cookies:
                self.session.cookies.set(c["name"], c["value"], domain=c.get("domain"))
            logger.debug("Loaded %d cookies from %s", len(cookies), PE_COOKIE_FILE)
        except Exception as exc:
            logger.warning("Could not load cookie file %s: %s", PE_COOKIE_FILE, exc)

    def _save_cookies(self) -> None:
        """Persist current session cookies to cookies.json for future runs."""
        if not PE_COOKIE_FILE:
            return
        PE_COOKIE_FILE.parent.mkdir(parents=True, exist_ok=True)
        cookies = [
            {"name": c.name, "value": c.value, "domain": c.domain}
            for c in self.session.cookies
        ]
        PE_COOKIE_FILE.write_text(json.dumps(cookies, indent=2), encoding="utf-8")
        logger.debug("Saved %d cookies to %s", len(cookies), PE_COOKIE_FILE)

    def _is_session_valid(self) -> bool:
        """Return True if the current session is already authenticated."""
        try:
            resp = self.session.get(f"{_BASE}/account", timeout=15, allow_redirects=True)
            soup = BeautifulSoup(resp.text, "lxml")
            return bool(soup.find("a", href=lambda h: h and "sign_out" in h))
        except Exception:
            return False

    def login(self) -> bool:
        """Log into Project Euler"""
        if self._is_session_valid():
            logger.info("Session cookie still valid - skipping login form")
            self._logged_in = True
            return True

        logger.info("Saved session expired or missing - attempting form login")
        resp = self.session.get(_LOGIN_URL, timeout=30)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "lxml")

        form = soup.find("form", method=lambda m: m and m.lower() == "post")
        if form is None:
            logger.error("Login form not found on sign-in page")
            return False

        # Collect all form fields (includes hidden CSRF tokens etc.)
        payload: dict[str, str] = {}
        for inp in form.find_all("input"):
            name = inp.get("name")
            if name:
                payload[name] = inp.get("value", "")

        payload["username"] = PE_USERNAME
        payload["password"] = PE_PASSWORD

        submit_btn = form.find("input", {"type": "submit"})
        if submit_btn and submit_btn.get("name"):
            payload[submit_btn["name"]] = submit_btn.get("value", "Sign In")

        action = form.get("action") or _LOGIN_URL
        if not action.startswith("http"):
            action = _BASE + "/" + action.lstrip("/")

        resp = self.session.post(action, data=payload, timeout=30, allow_redirects=True)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "lxml")
        signed_in = bool(soup.find("a", href=lambda h: h and "sign_out" in h))
        if signed_in:
            logger.info("Logged in to Project Euler as %s via form", PE_USERNAME)
            self._logged_in = True
            self._save_cookies()  # persist so the next run skips the form
            return True

        logger.error(
            "Form login failed. If a CAPTCHA was shown, run:\n"
            "  python -m automation.export_cookies\n"
            "to refresh your session cookies."
        )
        return False

    def get_problem(self, number: int) -> dict:
        """Get problem and download any additional data files"""
        url = f"{_BASE}/problem={number}"
        resp = self.session.get(url, timeout=30)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "lxml")

        # Title lives in an <h2> tag
        h2 = soup.find("h2")
        title = h2.get_text(strip=True) if h2 else f"Problem {number}"

        # Problem content div
        content_div = (
            soup.find("div", class_="problem_content")
            or soup.find("div", id="problem_content")
        )
        if content_div is None:
            raise RuntimeError(
                f"Could not locate problem content for problem {number}. "
                "The page structure may have changed."
            )

        # Download any supplemental data files linked from the problem.
        downloaded = self._download_supplemental_files(content_div, url)

        content_html = str(content_div)
        # Replace <br> / <p> with newlines for cleaner plain text
        for tag in content_div.find_all(["br", "p"]):
            tag.insert_before("\n")
        plain_text = content_div.get_text(separator=" ", strip=True)

        return {
            "number": number,
            "title": title,
            "text": plain_text,
            "content_html": content_html,
            "downloaded_files": downloaded,
        }

    def _download_supplemental_files(self, content_div, page_url: str) -> list[str]:
        dest_dir: Path = REPO_ROOT / "additional_files"
        dest_dir.mkdir(exist_ok=True)

        found: list[str] = []
        for anchor in content_div.find_all("a", href=True):
            href: str = anchor["href"]
            # Resolve relative URLs against the problem page
            full_url = urljoin(page_url, href)
            parsed = urlparse(full_url)
            suffix = Path(parsed.path).suffix.lower()
            if suffix not in _DATA_EXTENSIONS:
                continue

            filename = Path(parsed.path).name
            dest = dest_dir / filename

            if dest.exists():
                logger.debug("Supplemental file already exists: %s", filename)
            else:
                logger.info("Downloading supplemental file: %s", full_url)
                file_resp = self.session.get(full_url, timeout=60)
                file_resp.raise_for_status()
                dest.write_bytes(file_resp.content)
                logger.info("Saved %s (%d bytes)", filename, len(file_resp.content))

            found.append(filename)

        return found

    def submit_answer(self, problem_number: int, answer: str) -> bool:
        """Submit *answer* for *problem_number* - returns True if Project Euler accepts it as correct"""
        if not self._logged_in:
            raise RuntimeError("Must be logged in before submitting answers")

        url = f"{_BASE}/problem={problem_number}"
        resp = self.session.get(url, timeout=30)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "lxml")

        form = soup.find("form", method=lambda m: m and m.lower() == "post")
        if form is None:
            raise RuntimeError(
                f"Answer submission form not found for problem {problem_number}"
            )

        payload: dict[str, str] = {}
        for inp in form.find_all("input"):
            name = inp.get("name")
            if name:
                payload[name] = inp.get("value", "")

        # Locate the answer input field (named "guess", "guess_N", or similar)
        guess_field: Optional[str] = None
        for name in list(payload.keys()):
            if "guess" in name.lower():
                guess_field = name
                break
        if guess_field is None:
            for inp in form.find_all("input", {"type": "text"}):
                if inp.get("name"):
                    guess_field = inp["name"]
                    payload.setdefault(guess_field, "")
                    break
        if guess_field is None:
            raise RuntimeError(
                f"Cannot locate answer field in form for problem {problem_number}"
            )

        payload[guess_field] = str(answer).strip()

        action = form.get("action") or url
        if not action.startswith("http"):
            action = _BASE + "/" + action.lstrip("/")

        resp = self.session.post(action, data=payload, timeout=30, allow_redirects=True)
        resp.raise_for_status()

        body = resp.text.lower()
        # Already solved counts as correct – we just want the file saved and pushed.
        if any(kw in body for kw in [
            "congratulations", "correct answer", "is correct",
            "already solved", "you have already", "previously solved",
        ]):
            logger.info("Project Euler accepted the answer for problem %d", problem_number)
            return True
        if any(kw in body for kw in ["incorrect", "wrong", "is not correct", "not correct"]):
            logger.warning(
                "Project Euler rejected the answer '%s' for problem %d",
                answer,
                problem_number,
            )
            return False

        # Ambiguous – log the first 500 chars for debugging
        logger.warning(
            "Ambiguous response from Project Euler (problem %d). "
            "First 500 chars of body: %s",
            problem_number,
            resp.text[:500],
        )
        return False