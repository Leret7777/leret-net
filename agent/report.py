#!/usr/bin/env python3
"""
agent/report.py — writes the daily report that's posted as a GitHub
issue after each run, so Leret gets a notification saying what the
agent did, with links to see it and a way to undo it.

Usage (from the repo root):
    python3 agent/report.py <base-commit> <published-commit-or-empty>

Prints the report (Markdown) to stdout. Changes nothing.
"""

import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://leret.me"


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, check=True,
                          capture_output=True, text=True).stdout


def todays_log_entry():
    """The newest entry in agent/LOG.md: from the first '## ' heading
    up to the next one."""
    path = os.path.join(ROOT, "agent", "LOG.md")
    if not os.path.exists(path):
        return ""
    lines = open(path, encoding="utf-8").read().splitlines()
    out, started = [], False
    for line in lines:
        if line.startswith("## "):
            if started:
                break
            started = True
            out.append("**" + line[3:].strip() + "**")
            continue
        if started:
            out.append(line)
    return "\n".join(out).strip()


def page_url(src_path):
    """src/pages/index.html -> https://leret.me/ ; src/posts/x.html ->
    https://leret.me/posts/x.html. Anything else -> None."""
    if src_path.startswith("src/posts/") and src_path.endswith(".html"):
        name = os.path.basename(src_path)
        if name.startswith("_"):
            return None
        return f"{SITE}/posts/{name}"
    if src_path.startswith("src/pages/") and src_path.endswith(".html"):
        name = os.path.basename(src_path)
        return SITE + "/" if name == "index.html" else f"{SITE}/{name}"
    return None


def main():
    base = sys.argv[1]
    commit = sys.argv[2] if len(sys.argv) > 2 else ""

    parts = []
    if not commit:
        parts.append("**No changes today.** The site was checked and "
                     "everything was fine, or there was nothing new to add.")
        entry = todays_log_entry()
        if entry:
            parts.append(entry)
    else:
        entry = todays_log_entry()
        parts.append("### What the agent did\n\n" + (entry or "_No log entry written._"))

        changed = git("diff", "--name-status", base, commit).splitlines()
        pages, design, other = [], False, []
        for row in changed:
            status, _, path = row.partition("\t")
            path = path.split("\t")[-1]  # renames list old<TAB>new
            url = page_url(path)
            if url:
                word = {"A": "new", "D": "removed"}.get(status[0], "changed")
                pages.append(f"- [{url.replace(SITE, 'leret.me')}]({url}) ({word})")
            elif path in ("src/style.css", "src/script.js") or path.startswith("src/partials/"):
                design = True
            elif path.startswith("src/images/"):
                other.append(path)

        lines = []
        if pages:
            lines.extend(pages)
        if design:
            lines.append("- The look of the whole site (styles or shared layout)")
        if other:
            lines.append(f"- {len(other)} image file(s)")
        if lines:
            parts.append("### Pages to look at\n\n" + "\n".join(lines)
                         + "\n\nGive it a couple of minutes to go live.")

        parts.append(
            "### Don't like something?\n\n"
            "Reply to this issue:\n"
            "- **`undo`** puts the site back to how it was before today's run.\n"
            "- **Or say what to undo in your own words**, e.g. "
            "\"remove the new post\" or \"undo the menu change\", and only that "
            "part is undone.\n\n"
            "Either way, the agent is told not to do it again."
        )
        parts.append(f"<sub>Change: {commit[:7]}</sub>\n\n"
                     f"<!-- site-agent-commit: {commit} -->")

    print("\n\n".join(parts))


if __name__ == "__main__":
    main()
