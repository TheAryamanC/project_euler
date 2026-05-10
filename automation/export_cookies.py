#!/usr/bin/env python3
"""Cookie exporter"""

import base64
import json
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).parent.parent.resolve()
PE_COOKIE_FILE = _REPO_ROOT / "automation" / "cookies.json"

_BASE = "https://projecteuler.net"
_LOGIN_URL = f"{_BASE}/sign_in"


def _save_and_print(pe_cookies: list[dict]) -> None:
    PE_COOKIE_FILE.parent.mkdir(parents=True, exist_ok=True)
    PE_COOKIE_FILE.write_text(json.dumps(pe_cookies, indent=2), encoding="utf-8")
    print(f"\nSaved {len(pe_cookies)} cookies to {PE_COOKIE_FILE}")

    encoded = base64.b64encode(PE_COOKIE_FILE.read_bytes()).decode()
    print("\n" + "=" * 60)
    print("Paste this as the GitHub secret  PE_COOKIES_B64 :")
    print("=" * 60)
    print(encoded)
    print("=" * 60)
    print(
        "\nGitHub repo → Settings → Secrets and variables → Actions\n"
        "  Name:  PE_COOKIES_B64\n"
        "  Value: (the block above)\n"
    )


def _browser_mode() -> None:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print(
            "Playwright not found. Install with:\n"
            "  pip install playwright && playwright install chromium\n"
            "Or use --manual if you have no display."
        )
        sys.exit(1)

    print("A Chromium window will open. Log in to Project Euler normally.")
    print("Solve any CAPTCHA. The script detects the login automatically.")
    print("Press Ctrl+C to cancel.\n")

    raw_cookies: list = []

    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=False, slow_mo=50)
            ctx = browser.new_context()
            page = ctx.new_page()
            page.goto(_LOGIN_URL, timeout=30_000)

            print("Waiting for login", end="", flush=True)
            while True:
                try:
                    page.wait_for_timeout(2_000)

                    # Check current URL and page content without navigating
                    current_url = page.url
                    content = page.content().lower()

                    not_on_login = "sign_in" not in current_url
                    has_logged_in_content = any([
                        "sign_out" in content,
                        "sign out" in content,
                        "problems solved" in content,
                        "your account" in content,
                        "level " in content,
                    ])

                    if not_on_login and has_logged_in_content:
                        break

                    print(".", end="", flush=True)

                except KeyboardInterrupt:
                    raise
                except Exception:
                    print("\nBrowser closed before login detected. Try again.")
                    sys.exit(1)

            print("\nLogin detected — extracting cookies...")
            raw_cookies = ctx.cookies()
            browser.close()

    except KeyboardInterrupt:
        print("\nCancelled.")
        sys.exit(0)

    pe_cookies = [
        {"name": c["name"], "value": c["value"], "domain": c["domain"]}
        for c in raw_cookies
        if "projecteuler" in c.get("domain", "")
    ]

    if not pe_cookies:
        print("ERROR: No Project Euler cookies found. Did the login succeed?")
        sys.exit(1)

    _save_and_print(pe_cookies)


def _manual_mode() -> None:
    print(
        "\nMANUAL MODE\n"
        "-----------\n"
        "1. Open  https://projecteuler.net/sign_in  in your own browser.\n"
        "2. Log in and solve any CAPTCHA.\n"
        "3. Open Developer Tools:\n"
        "     Chrome/Edge: F12 → Application → Cookies → https://projecteuler.net\n"
        "     Firefox:     F12 → Storage → Cookies → https://projecteuler.net\n"
        "4. Find the cookie named  PHPSESSID  and copy its Value.\n"
    )
    try:
        phpsessid = input("Paste PHPSESSID value: ").strip()
    except KeyboardInterrupt:
        print("\nCancelled.")
        sys.exit(0)

    if not phpsessid:
        print("No value entered — aborting.")
        sys.exit(1)

    print("\n(Optional) Also copy  keep_alive  if it exists, or press Enter to skip.")
    try:
        keep_alive = input("keep_alive value (or Enter): ").strip()
    except KeyboardInterrupt:
        keep_alive = ""

    pe_cookies: list[dict] = [
        {"name": "PHPSESSID", "value": phpsessid, "domain": "projecteuler.net"},
    ]
    if keep_alive:
        pe_cookies.append(
            {"name": "keep_alive", "value": keep_alive, "domain": "projecteuler.net"}
        )

    _save_and_print(pe_cookies)


def main() -> None:
    if "--manual" in sys.argv:
        _manual_mode()
    else:
        _browser_mode()


if __name__ == "__main__":
    main()