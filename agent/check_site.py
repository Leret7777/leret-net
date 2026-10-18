#!/usr/bin/env python3
"""
agent/check_site.py — the site agent's daily health check.

Run it from the repo root AFTER `python3 build.py`:

    python3 agent/check_site.py            # internal checks only
    python3 agent/check_site.py --external # also test links to other sites

It reads the finished site in docs/ and prints a plain-English report of
anything broken or unfinished. It changes nothing. The agent reads this
report and decides what to fix; this script just finds the problems.

Standard library only, like build.py.
"""

import os
import sys
import urllib.request
import urllib.error
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")

# Text that means "a human still needs to fill this in".
PLACEHOLDER_MARKERS = [
    "REPLACE_WITH",
    "Your Post Title Here",
    "lorem ipsum",
    "TODO",
]

# Pages heavier than this (bytes) are flagged as slow to load.
MAX_IMAGE_BYTES = 500_000


class LinkCollector(HTMLParser):
    """Collects every href/src on a page, plus <img> tags missing alt."""

    def __init__(self):
        super().__init__()
        self.links = []          # (attr, value)
        self.imgs_no_alt = 0
        self.has_title = False
        self.has_description = False
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        for key in ("href", "src"):
            if key in attrs and attrs[key] is not None:
                self.links.append((key, attrs[key].strip()))
        if tag == "img" and "alt" not in attrs:
            self.imgs_no_alt += 1
        if tag == "title":
            self._in_title = True
        if tag == "meta" and attrs.get("name") == "description" and attrs.get("content"):
            self.has_description = True

    def handle_data(self, data):
        if self._in_title and data.strip():
            self.has_title = True

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False


def resolve_internal(page_path, link):
    """Turn a site link into a file path inside docs/, or None if it
    isn't an internal file link."""
    link = link.split("#", 1)[0].split("?", 1)[0]
    if not link:
        return None
    if link.startswith("/"):
        target = os.path.join(DOCS, link.lstrip("/"))
    else:
        target = os.path.join(os.path.dirname(page_path), link)
    if link.endswith("/") or os.path.isdir(target):
        target = os.path.join(target, "index.html")
    return os.path.normpath(target)


def check_external(url):
    req = urllib.request.Request(url, method="HEAD",
                                 headers={"User-Agent": "leret.me site check"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status < 400, resp.status
    except urllib.error.HTTPError as e:
        # Some sites refuse HEAD or bots (403/405/429) but work in a browser.
        if e.code in (403, 405, 429, 999):
            return True, e.code
        return False, e.code
    except Exception as e:  # timeouts, DNS failures, etc.
        return False, type(e).__name__


def main():
    external = "--external" in sys.argv
    if not os.path.isdir(DOCS):
        print("ERROR: docs/ not found. Run `python3 build.py` first.")
        return 1

    problems = []
    external_links = set()
    pages = 0

    for dirpath, _, files in os.walk(DOCS):
        for name in files:
            path = os.path.join(dirpath, name)
            rel = os.path.relpath(path, DOCS)

            if name.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                size = os.path.getsize(path)
                if size > MAX_IMAGE_BYTES:
                    problems.append(f"HEAVY IMAGE: {rel} is {size // 1000} KB "
                                    "(resize with scripts/resize_images.py)")
                continue

            if not name.endswith(".html"):
                continue
            pages += 1
            with open(path, encoding="utf-8") as f:
                html = f.read()

            parser = LinkCollector()
            parser.feed(html)

            if not parser.has_title:
                problems.append(f"MISSING TITLE: {rel} has no <title>")
            if not parser.has_description:
                problems.append(f"MISSING DESCRIPTION: {rel} has no meta description")
            if parser.imgs_no_alt:
                problems.append(f"MISSING ALT TEXT: {rel} has {parser.imgs_no_alt} image(s) without alt")

            for marker in PLACEHOLDER_MARKERS:
                if marker.lower() in html.lower():
                    problems.append(f"PLACEHOLDER TEXT: {rel} contains '{marker}'")

            for attr, link in parser.links:
                if link == "#" and attr == "href":
                    problems.append(f"PLACEHOLDER LINK: {rel} has a link pointing nowhere (href=\"#\")")
                    continue
                if link.startswith(("mailto:", "tel:", "data:", "javascript:", "#")):
                    continue
                if link.startswith(("http://", "https://")):
                    external_links.add(link)
                    continue
                if link.startswith("//"):
                    external_links.add("https:" + link)
                    continue
                target = resolve_internal(path, link)
                if target and not os.path.exists(target):
                    problems.append(f"BROKEN LINK: {rel} -> {link} (file not found)")

    if external:
        for url in sorted(external_links):
            # Share-link endpoints and font CDNs aren't worth testing.
            if "sharing/share-offsite" in url or "fonts.g" in url:
                continue
            ok, status = check_external(url)
            if not ok:
                problems.append(f"BROKEN EXTERNAL LINK: {url} ({status})")

    # De-duplicate while keeping order.
    seen = set()
    problems = [p for p in problems if not (p in seen or seen.add(p))]

    print(f"Checked {pages} pages"
          + (f" and {len(external_links)} external links" if external else ""))
    if not problems:
        print("No problems found.")
    else:
        print(f"{len(problems)} problem(s):")
        for p in problems:
            print(" - " + p)
    return 0


if __name__ == "__main__":
    sys.exit(main())
