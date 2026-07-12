#!/usr/bin/env python3
"""
build.py — turns src/ into docs/ (the folder GitHub Pages actually serves).

Run this locally after editing anything in src/, then commit both src/ and
docs/ and push. There is no build server and no CI — this script IS the
whole "build step".

What it does, in order:
  1. Wipes docs/ and starts clean, so nothing stale lingers between builds.
  2. Reads the two shared partials (nav.html, footer.html) once.
  3. For every page in src/pages/, swaps the <!-- NAV --> and
     <!-- FOOTER --> placeholder comments for the real partial markup,
     and writes the result into docs/.
  4. For every post in src/posts/, reads a small metadata comment at the
     very top of the file (title + date), does the same nav/footer
     injection, and writes it into docs/posts/.
  5. Uses the metadata gathered in step 4 to auto-generate the post list
     on the Writing page (sorted newest first) and drops it into the
     <!-- POST_LIST --> placeholder inside writing.html.
  6. Copies static assets (style.css, script.js, the images folder, and
     CNAME) into docs/ untouched.

Everything here uses plain string methods (str.find, str.replace,
str.split, slicing) — no regex, no templating library, no pip installs.
That's deliberate: you should be able to read this file top to bottom and
know exactly what happened to your HTML.
"""

import os
import shutil

# ---------------------------------------------------------------------------
# Paths. Keeping them all in one place means if you ever rename a folder,
# there's exactly one line to change.
# ---------------------------------------------------------------------------
ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")
PAGES_DIR = os.path.join(SRC, "pages")
PARTIALS_DIR = os.path.join(SRC, "partials")
POSTS_DIR = os.path.join(SRC, "posts")
IMAGES_DIR = os.path.join(SRC, "images")
DOCS = os.path.join(ROOT, "docs")
POSTS_OUT_DIR = os.path.join(DOCS, "posts")

NAV_PLACEHOLDER = "<!-- NAV -->"
FOOTER_PLACEHOLDER = "<!-- FOOTER -->"
POST_LIST_PLACEHOLDER = "<!-- POST_LIST -->"


def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_file(path, content):
    # Make sure the destination folder exists before writing into it —
    # os.makedirs with exist_ok=True is a no-op if it's already there.
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def inject_partials(html, nav_html, footer_html):
    """Replace the placeholder comments with the real shared markup.

    str.replace swaps *every* occurrence of the placeholder text, which is
    exactly what we want since a page only ever has one NAV and one
    FOOTER placeholder.
    """
    html = html.replace(NAV_PLACEHOLDER, nav_html)
    html = html.replace(FOOTER_PLACEHOLDER, footer_html)
    return html


# ---------------------------------------------------------------------------
# Post metadata parsing
# ---------------------------------------------------------------------------
# Every file in src/posts/ starts with a small HTML comment like:
#
#   <!-- POST META
#   title: Why I Started Writing
#   date: 2026-01-15
#   -->
#   <!DOCTYPE html>
#   ...
#
# We pull the title/date out of that comment for the Writing page listing,
# then strip the comment out before injecting nav/footer, so the comment
# never ends up in the published HTML.

META_START = "<!-- POST META"
META_END = "-->"


def parse_post(html):
    """Split a post file into (title, date, remaining_html).

    remaining_html is everything after the metadata comment — i.e. the
    actual page, starting at <!DOCTYPE html>.
    """
    start = html.find(META_START)
    if start == -1:
        raise ValueError("Post is missing a <!-- POST META ... --> comment at the top")

    end = html.find(META_END, start)
    if end == -1:
        raise ValueError("Post's POST META comment is never closed with -->")

    # The metadata block is the text between the start marker and "-->".
    meta_block = html[start + len(META_START):end]
    remaining_html = html[end + len(META_END):].lstrip("\n")

    title = None
    date = None
    for line in meta_block.splitlines():
        line = line.strip()
        if line.startswith("title:"):
            title = line[len("title:"):].strip()
        elif line.startswith("date:"):
            date = line[len("date:"):].strip()

    if not title or not date:
        raise ValueError("Post metadata must include both 'title:' and 'date:'")

    return title, date, remaining_html


def build_post_list_html(posts):
    """posts is a list of (title, date, slug) tuples, already sorted.

    Returns an <ul> of links, ready to drop straight into writing.html.
    """
    if not posts:
        return "<p>No posts yet — check back soon.</p>"

    items = []
    for title, date, slug in posts:
        items.append(
            '      <li class="post-list__item">\n'
            f'        <a href="/posts/{slug}.html">{title}</a>\n'
            f'        <span class="post-date">{date}</span>\n'
            "      </li>"
        )
    return "<ul class=\"post-list\">\n" + "\n".join(items) + "\n    </ul>"


def build():
    # 1. Start from a clean docs/ folder every time, so deleted/renamed
    #    pages don't leave orphaned files behind.
    if os.path.exists(DOCS):
        shutil.rmtree(DOCS)
    os.makedirs(DOCS)

    # 2. Load the shared partials once — every page reuses the same string.
    nav_html = read_file(os.path.join(PARTIALS_DIR, "nav.html"))
    footer_html = read_file(os.path.join(PARTIALS_DIR, "footer.html"))

    # 3. Build every post first, because we need each post's title/date/slug
    #    before we can generate the Writing page's listing in step 4.
    posts = []  # list of (title, date, slug)
    if os.path.isdir(POSTS_DIR):
        for filename in os.listdir(POSTS_DIR):
            if not filename.endswith(".html"):
                continue
            slug = filename[: -len(".html")]
            raw = read_file(os.path.join(POSTS_DIR, filename))
            title, date, page_html = parse_post(raw)
            final_html = inject_partials(page_html, nav_html, footer_html)
            write_file(os.path.join(POSTS_OUT_DIR, filename), final_html)
            posts.append((title, date, slug))

    # Sort newest first. Dates are written as YYYY-MM-DD, so plain string
    # sorting already puts them in chronological order — reverse=True
    # flips that to newest-first.
    posts.sort(key=lambda p: p[1], reverse=True)
    post_list_html = build_post_list_html(posts)

    # 4. Build every regular page in src/pages/.
    for filename in os.listdir(PAGES_DIR):
        if not filename.endswith(".html"):
            continue
        raw = read_file(os.path.join(PAGES_DIR, filename))
        final_html = inject_partials(raw, nav_html, footer_html)

        # Only writing.html has a post list to fill in; on every other
        # page this placeholder simply won't be present, so replace()
        # does nothing.
        final_html = final_html.replace(POST_LIST_PLACEHOLDER, post_list_html)

        write_file(os.path.join(DOCS, filename), final_html)

    # 5. Copy static assets across untouched.
    shutil.copy(os.path.join(SRC, "style.css"), os.path.join(DOCS, "style.css"))
    shutil.copy(os.path.join(SRC, "script.js"), os.path.join(DOCS, "script.js"))

    if os.path.isdir(IMAGES_DIR):
        shutil.copytree(IMAGES_DIR, os.path.join(DOCS, "images"))

    # 6. Copy CNAME so the custom domain survives every rebuild (docs/ is
    #    wiped in step 1, so this has to happen on every run, not just once).
    cname_path = os.path.join(ROOT, "CNAME")
    if os.path.exists(cname_path):
        shutil.copy(cname_path, os.path.join(DOCS, "CNAME"))

    print(f"Built {len(os.listdir(PAGES_DIR))} pages and {len(posts)} posts into docs/")


if __name__ == "__main__":
    build()
