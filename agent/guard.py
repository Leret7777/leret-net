#!/usr/bin/env python3
"""
agent/guard.py — the safety check that runs AFTER the agent and BEFORE
anything is published. The agent can't skip it: it's a separate step in
the GitHub workflow, not something the agent is asked to do.

Usage (from the repo root):  python3 agent/guard.py <commit-before-agent>

It:
  1. Undoes any change the agent made outside the folders it's allowed
     to touch (so it can never edit the workflow, build.py, CNAME, etc.).
  2. Refuses to publish if a post was deleted.
  3. Rebuilds the site and refuses to publish if the build fails or the
     homepage / custom domain went missing.

Exit code 0 = safe to publish. Anything else = the run stops, nothing
goes live, and the failure shows up in the GitHub Actions tab.
"""

import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# The only places the agent may change. Everything else is put back.
ALLOWED_PREFIXES = (
    "src/",
    "inbox/",
    "agent/LOG.md",
    "agent/NEEDS_FROM_LERET.md",
    "agent/SOURCES.md",   # only from Leret's inbox notes (see BRIEF.md)
    "agent/STYLE.md",     # only to tick off roadmap items
    "README.md",
)


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, check=True,
                          capture_output=True, text=True).stdout


def changed_paths(base):
    # Tracked changes (committed or not) since base, plus brand-new files.
    tracked = git("diff", "--name-only", base).split()
    untracked = git("ls-files", "--others", "--exclude-standard").split()
    return sorted(set(tracked + untracked))


def post_slugs_at(base):
    out = git("ls-tree", "--name-only", f"{base}:src/posts")
    return {n for n in out.split() if n.endswith(".html") and not n.startswith("_")}


def main():
    if len(sys.argv) not in (2, 3):
        print("usage: python3 agent/guard.py <base-commit> [<commit-being-undone>]")
        return 2
    base = sys.argv[1]
    # When undoing a day, posts that day ADDED are allowed to go again.
    undoing = sys.argv[2] if len(sys.argv) == 3 else ""
    added_that_day = set()
    if undoing:
        out = git("diff", "--name-only", "--diff-filter=A",
                  f"{undoing}~1", undoing, "--", "src/posts")
        added_that_day = {os.path.basename(p) for p in out.split()}

    # 1. Put back anything outside the allowed folders.
    reverted = []
    for path in changed_paths(base):
        if path.startswith("docs/"):
            continue  # docs/ is regenerated below anyway
        if path.startswith(ALLOWED_PREFIXES):
            continue
        reverted.append(path)
        exists_in_base = subprocess.run(
            ["git", "cat-file", "-e", f"{base}:{path}"], cwd=ROOT,
            stderr=subprocess.DEVNULL).returncode == 0
        if exists_in_base:
            git("checkout", base, "--", path)
        else:
            os.remove(os.path.join(ROOT, path))
    if reverted:
        print("Undid changes outside the allowed folders:")
        for p in reverted:
            print("  - " + p)

    # 2. No post may disappear.
    before = post_slugs_at(base)
    posts_dir = os.path.join(ROOT, "src", "posts")
    after = {n for n in os.listdir(posts_dir)
             if n.endswith(".html") and not n.startswith("_")}
    missing = before - after - added_that_day
    if missing:
        print("STOP: these posts were deleted: " + ", ".join(sorted(missing)))
        return 1

    # 3. The site must still build, with its homepage and domain intact.
    result = subprocess.run([sys.executable, "build.py"], cwd=ROOT,
                            capture_output=True, text=True)
    print(result.stdout.strip())
    if result.returncode != 0:
        print("STOP: build.py failed:\n" + result.stderr)
        return 1
    for must_exist in ("docs/index.html", "docs/about.html", "docs/CNAME"):
        if not os.path.exists(os.path.join(ROOT, must_exist)):
            print(f"STOP: {must_exist} is missing after the build")
            return 1
    with open(os.path.join(ROOT, "docs", "CNAME"), encoding="utf-8") as f:
        if f.read().strip() != "leret.me":
            print("STOP: docs/CNAME no longer says leret.me")
            return 1

    print("Guard passed: safe to publish.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
