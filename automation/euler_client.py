import logging
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

from .config import REPO_ROOT

_DATA_EXTENSIONS = {".txt", ".csv", ".dat", ".gz", ".zip", ".rtf"}  # supplemental files

logger = logging.getLogger(__name__)

_BASE = "https://projecteuler.net"
_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}


class ProjectEulerClient:
    """Read-only HTTP client for fetching public Project Euler problems.

    Project Euler problem statements are public, so this client performs no login
    and no answer submission. It only downloads the problem text (and any
    supplemental data files) so the solver can produce and commit a solution.
    """

    def __init__(self) -> None:
        self.session = requests.Session()
        self.session.headers.update(_HEADERS)

    def get_problem(self, number: int) -> dict:
        """Fetch a problem and download any additional data files it references."""
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
            # Fall back to the public minimal endpoint, which returns just the raw
            # problem HTML fragment (no page chrome). This is more stable than the
            # full page layout.
            logger.info(
                "problem_content div not found on full page for problem %d; "
                "falling back to the public minimal=%d endpoint",
                number,
                number,
            )
            minimal = self.session.get(f"{_BASE}/minimal={number}", timeout=30)
            minimal.raise_for_status()
            content_div = BeautifulSoup(f"<div>{minimal.text}</div>", "lxml").find("div")
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
