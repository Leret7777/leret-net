#!/usr/bin/env python3
"""
build.py — turns src/ into docs/ (the folder GitHub Pages actually serves).

Run this locally after editing anything in src/, then commit both src/ and
docs/ and push. There is no build server and no CI — this script IS the
whole "build step".

What it does, in order:
  1. Wipes docs/ and starts clean, so nothing stale lingers between builds.
  2. Reads the two shared partials (nav.html, footer.html) once.
  3. For every post in src/posts/, reads the metadata comment at the very
     top (title, date, tags, excerpt), swaps the <!-- NAV --> and
     <!-- FOOTER --> placeholders for the shared partial markup, and
     writes the result into docs/posts/.
  4. Builds the homepage post list (newest first, with tag labels and
     excerpts) and the tag filter row, and injects them into index.html
     at the <!-- POST_LIST --> and <!-- TAG_FILTERS --> placeholders.
  5. Writes docs/posts-index.json — a machine-readable list of every
     post (title, date, tags, url, excerpt) that the client-side search
     could use, and that makes the post data easy to reuse anywhere else.
  6. Builds every page in src/pages/ with the same nav/footer injection.
  7. Copies static assets (style.css, script.js, images/, CNAME) into
     docs/ untouched.

Everything here uses plain string methods (str.find, str.split,
str.replace, slicing) plus the standard-library json module — no regex,
no templating library, no pip installs. You should be able to read this
file top to bottom and know exactly what happened to your HTML.
"""

import json
import os
import shutil
import urllib.parse

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
TAG_FILTERS_PLACEHOLDER = "<!-- TAG_FILTERS -->"
CONTACT_LINKS_PLACEHOLDER = "<!-- CONTACT_LINKS -->"
NEWSLETTER_PLACEHOLDER = "<!-- NEWSLETTER -->"

# The site's public address — used to build absolute URLs for the
# social share links (a share link has to tell X/LinkedIn/WhatsApp the
# full address of the page, not a relative path).
SITE_URL = "https://leret.me"


def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_file(path, content):
    # Make sure the destination folder exists before writing into it —
    # os.makedirs with exist_ok=True is a no-op if it's already there.
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def inject_partials(html, nav_html, footer_html, contact_links_html,
                    newsletter_html):
    """Replace the placeholder comments with the real shared markup.

    CONTACT_LINKS is replaced *after* the footer, on purpose: the footer
    partial itself contains a CONTACT_LINKS placeholder, so the footer
    has to be pasted into the page first for that inner placeholder to
    be present and get filled in. Same icons, maintained in one file,
    appearing in both the homepage intro and every footer.
    """
    html = html.replace(NAV_PLACEHOLDER, nav_html)
    html = html.replace(FOOTER_PLACEHOLDER, footer_html)
    html = html.replace(CONTACT_LINKS_PLACEHOLDER, contact_links_html)
    html = html.replace(NEWSLETTER_PLACEHOLDER, newsletter_html)
    return html


# ---------------------------------------------------------------------------
# Post metadata parsing
# ---------------------------------------------------------------------------
# Every file in src/posts/ starts with a single-line HTML comment holding
# its metadata, with fields separated by pipes:
#
#   <!-- title: My Post Title | date: 2026-07-14 | tags: modeling, work | excerpt: One short line about the post. -->
#   <!DOCTYPE html>
#   ...
#
# Required fields: title, date (YYYY-MM-DD).
# Optional fields: tags (comma-separated — a post can have several, or
# none at all), excerpt (the one-liner shown under the title on the
# homepage list).
#
# We pull these out for the homepage listing and posts-index.json, then
# strip the comment before publishing, so it never appears in the
# rendered HTML.

META_START = "<!--"
META_END = "-->"


def parse_post(html, filename):
    """Split a post file into (metadata_dict, remaining_html).

    remaining_html is everything after the metadata comment — i.e. the
    actual page, starting at <!DOCTYPE html>.
    """
    start = html.find(META_START)
    end = html.find(META_END, start)
    if start == -1 or end == -1 or "title:" not in html[start:end]:
        raise ValueError(f"{filename}: missing metadata comment at the top "
                         "(<!-- title: ... | date: ... -->)")

    meta_block = html[start + len(META_START):end]
    remaining_html = html[end + len(META_END):].lstrip("\n")

    # Split "title: X | date: Y | tags: a, b" into fields, then each
    # field into key/value at its FIRST colon (str.partition), so
    # excerpts containing colons still parse correctly.
    meta = {}
    for field in meta_block.split("|"):
        field = field.strip()
        if not field or ":" not in field:
            continue
        key, _, value = field.partition(":")
        meta[key.strip().lower()] = value.strip()

    if "title" not in meta or "date" not in meta:
        raise ValueError(f"{filename}: metadata must include both 'title:' and 'date:'")

    # Normalize tags into a list: "modeling, work" -> ["modeling", "work"].
    # Lowercased so filtering isn't case-sensitive; empty if no tags field.
    tags_value = meta.get("tags", "")
    meta["tags"] = [t.strip().lower() for t in tags_value.split(",") if t.strip()]
    meta["excerpt"] = meta.get("excerpt", "")

    return meta, remaining_html


def build_post_list_html(posts):
    """posts is a list of metadata dicts (each with a 'slug' added),
    already sorted newest-first. Returns the homepage <ul>.

    Each <li> carries a data-tags attribute (comma-separated) that the
    client-side filter JS reads — data-* attributes are how HTML lets
    you attach machine-readable info to an element without affecting
    how it displays.
    """
    if not posts:
        return "<p>No posts yet — check back soon.</p>"

    items = []
    for post in posts:
        tags_attr = ",".join(post["tags"])

        tag_labels = ""
        if post["tags"]:
            labels = "".join(f"<li>{tag}</li>" for tag in post["tags"])
            tag_labels = f'\n        <ul class="post-tags">{labels}</ul>'

        excerpt_html = ""
        if post["excerpt"]:
            excerpt_html = f'\n        <p class="post-excerpt">{post["excerpt"]}</p>'

        items.append(
            f'      <li class="post-list__item" data-tags="{tags_attr}">\n'
            f'        <div class="post-list__head">\n'
            f'          <a href="/posts/{post["slug"]}.html">{post["title"]}</a>\n'
            f'          <span class="post-date">{post["date"]}</span>\n'
            f'        </div>{tag_labels}{excerpt_html}\n'
            "      </li>"
        )
    return '<ul class="post-list" id="postList">\n' + "\n".join(items) + "\n    </ul>"


def build_tag_filters_html(posts):
    """Collect every tag used by any post and render the filter row.

    The tag list is derived from the posts themselves — nothing is
    hardcoded, so tagging a post with something new automatically adds
    a filter button on the next build.
    """
    all_tags = set()
    for post in posts:
        all_tags.update(post["tags"])

    buttons = ['<button class="tag-filter is-active" data-tag="all">All</button>']
    for tag in sorted(all_tags):
        buttons.append(f'<button class="tag-filter" data-tag="{tag}">{tag}</button>')

    return ('<div class="tag-filters" id="tagFilters">\n      '
            + "\n      ".join(buttons)
            + "\n    </div>")


# ---------------------------------------------------------------------------
# Post ending block
# ---------------------------------------------------------------------------
# Every post gets an auto-generated ending: newsletter signup, the post's
# tag(s) as filter links, a share row, a back-to-top link, and
# previous/next post navigation. It's generated here (not hand-written in
# each post) because it needs things an individual post file can't know:
# the neighbouring posts in date order, and the post's own metadata.

# Share links are just URLs — each platform publishes an address that
# takes ?url= / ?text= parameters and opens its "compose" screen
# pre-filled. urllib.parse.quote percent-encodes the title/URL so
# spaces and punctuation survive being embedded inside another URL.

SHARE_ICONS = {
    # Solid brand glyphs (Simple Icons, CC0), drawn with fill rather
    # than stroke so the marks stay recognisable at 26px.
    "x": '<svg viewBox="0 0 24 24" width="26" height="26" fill="currentColor" aria-hidden="true"><path d="M18.9 1.15h3.68l-8.04 9.19L24 22.85h-7.41l-5.8-7.58-6.64 7.58H.47l8.6-9.83L0 1.15h7.59l5.24 6.93zm-1.29 19.5h2.04L6.48 3.24H4.3z"/></svg>',
    "linkedin": '<svg viewBox="0 0 24 24" width="26" height="26" fill="currentColor" aria-hidden="true"><path d="M20.45 20.45h-3.55v-5.57c0-1.33-.03-3.04-1.85-3.04-1.85 0-2.14 1.45-2.14 2.94v5.67H9.36V9h3.41v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28zM5.34 7.43a2.06 2.06 0 1 1 0-4.13 2.06 2.06 0 0 1 0 4.13zM7.12 20.45H3.56V9h3.56v11.45zM22.22 0H1.77C.79 0 0 .77 0 1.72v20.55C0 23.23.79 24 1.77 24h20.45c.98 0 1.78-.77 1.78-1.73V1.72C24 .77 23.2 0 22.22 0z"/></svg>',
    "whatsapp": '<svg viewBox="0 0 24 24" width="26" height="26" fill="currentColor" aria-hidden="true"><path d="M17.47 14.38c-.3-.15-1.76-.87-2.03-.97-.27-.1-.47-.15-.67.15-.2.3-.77.96-.94 1.16-.17.2-.35.22-.64.08-.3-.15-1.26-.47-2.4-1.48-.88-.79-1.48-1.76-1.65-2.06-.17-.3-.02-.46.13-.6.13-.13.3-.35.44-.52.15-.17.2-.3.3-.5.1-.2.05-.37-.02-.52-.08-.15-.67-1.61-.92-2.21-.24-.58-.49-.5-.67-.51h-.57c-.2 0-.52.07-.8.37-.27.3-1.04 1.02-1.04 2.49 0 1.47 1.07 2.89 1.22 3.09.15.2 2.1 3.21 5.1 4.5.71.31 1.27.49 1.7.63.72.23 1.37.2 1.88.12.57-.09 1.76-.72 2-1.41.25-.7.25-1.29.18-1.42-.08-.13-.28-.2-.57-.35M12.05 21.79h-.01a9.87 9.87 0 0 1-5.03-1.38l-.36-.21-3.74.98 1-3.65-.24-.37a9.86 9.86 0 0 1-1.51-5.26c0-5.45 4.44-9.88 9.9-9.88a9.83 9.83 0 0 1 9.88 9.9c0 5.45-4.44 9.87-9.89 9.87M20.5 3.49A11.82 11.82 0 0 0 12.05 0C5.5 0 .16 5.34.16 11.9c0 2.1.55 4.14 1.6 5.95L.06 24l6.3-1.65a11.88 11.88 0 0 0 5.68 1.45h.01c6.55 0 11.89-5.34 11.89-11.9 0-3.18-1.24-6.16-3.44-8.4"/></svg>',
    "facebook": '<svg viewBox="0 0 24 24" width="26" height="26" fill="currentColor" aria-hidden="true"><path d="M24 12.07C24 5.4 18.63 0 12 0S0 5.4 0 12.07c0 6.02 4.39 11.02 10.13 11.93v-8.44H7.08v-3.49h3.04V9.41c0-3.02 1.8-4.7 4.55-4.7 1.31 0 2.68.24 2.68.24v2.97h-1.5c-1.5 0-1.96.93-1.96 1.87v2.25h3.32l-.53 3.49h-2.8V24C19.62 23.1 24 18.1 24 12.07"/></svg>',
    "email": '<svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2.5" y="4.5" width="19" height="15" rx="2.5"/><path d="m3.5 7 8.5 6 8.5-6"/></svg>',
}


def build_post_ending_html(post, prev_post, next_post, newsletter_html):
    """The block appended to every post, before the footer.

    prev_post is the older neighbour, next_post the newer one (either
    may be None at the ends of the timeline).
    """
    url = f"{SITE_URL}/posts/{post['slug']}.html"
    quoted_url = urllib.parse.quote(url, safe="")
    quoted_title = urllib.parse.quote(post["title"])

    share_links = [
        ("x", "Share on X",
         f"https://twitter.com/intent/tweet?url={quoted_url}&text={quoted_title}"),
        ("linkedin", "Share on LinkedIn",
         f"https://www.linkedin.com/sharing/share-offsite/?url={quoted_url}"),
        ("whatsapp", "Share on WhatsApp",
         f"https://wa.me/?text={quoted_title}%20{quoted_url}"),
        ("facebook", "Share on Facebook",
         f"https://www.facebook.com/sharer/sharer.php?u={quoted_url}"),
        ("email", "Share by email",
         f"mailto:?subject={quoted_title}&body={quoted_url}"),
    ]
    share_items = "\n        ".join(
        f'<li><a href="{href}" target="_blank" rel="noopener" aria-label="{label}">{SHARE_ICONS[icon]}</a></li>'
        for icon, label, href in share_links
    )

    tag_links = " ".join(
        f'<a class="post-ending__tag" href="/?tag={tag}">#{tag}</a>'
        for tag in post["tags"]
    )

    nav_parts = []
    if prev_post:
        nav_parts.append(
            '      <a class="post-nav__link post-nav__link--prev" '
            f'href="/posts/{prev_post["slug"]}.html">\n'
            '        <span class="post-nav__label">&larr; Previous post</span>\n'
            f'        <span class="post-nav__title">{prev_post["title"]}</span>\n'
            "      </a>"
        )
    if next_post:
        nav_parts.append(
            '      <a class="post-nav__link post-nav__link--next" '
            f'href="/posts/{next_post["slug"]}.html">\n'
            '        <span class="post-nav__label">Next post &rarr;</span>\n'
            f'        <span class="post-nav__title">{next_post["title"]}</span>\n'
            "      </a>"
        )
    post_nav = ""
    if nav_parts:
        post_nav = ('\n    <nav class="post-nav" aria-label="More posts">\n'
                    + "\n".join(nav_parts) + "\n    </nav>")

    return f"""<aside class="post-ending">
  <div class="wrap">
    {newsletter_html}
    <p class="post-ending__tags">{tag_links}</p>
    <div class="share-row">
      <p class="share-row__label">Share this post:</p>
      <ul class="share-row__icons">
        {share_items}
      </ul>
      <a class="back-to-top" href="#top">&uarr; Back to top</a>
    </div>{post_nav}
  </div>
</aside>
"""


def build():
    # 1. Start from a clean docs/ folder every time, so deleted/renamed
    #    pages don't leave orphaned files behind.
    if os.path.exists(DOCS):
        shutil.rmtree(DOCS)
    os.makedirs(DOCS)

    # 2. Load the shared partials once — every page reuses the same string.
    nav_html = read_file(os.path.join(PARTIALS_DIR, "nav.html"))
    footer_html = read_file(os.path.join(PARTIALS_DIR, "footer.html"))
    contact_links_html = read_file(os.path.join(PARTIALS_DIR, "contact-links.html"))
    newsletter_html = read_file(os.path.join(PARTIALS_DIR, "newsletter.html"))

    # 3. Build every post first — we need all the metadata before we can
    #    generate the homepage list, filter row, and JSON index.
    # Parse every post FIRST (without writing anything yet): each post's
    # ending block needs to know its neighbours in date order, so we
    # can't finish any single post until we've read them all.
    posts = []
    if os.path.isdir(POSTS_DIR):
        for filename in sorted(os.listdir(POSTS_DIR)):
            if not filename.endswith(".html"):
                continue
            raw = read_file(os.path.join(POSTS_DIR, filename))
            meta, page_html = parse_post(raw, filename)
            meta["slug"] = filename[: -len(".html")]
            meta["page_html"] = page_html

            # Current convention: every post carries exactly one tag.
            # This is a warning, not an error — the site still builds,
            # because the mechanism deliberately supports any number of
            # tags (that's what lets a new category appear just by
            # using it in a post).
            if len(meta["tags"]) != 1:
                print(f"  warning: {filename} has {len(meta['tags'])} tags "
                      f"(convention is exactly one)")
            posts.append(meta)

    # Sort newest first. Dates are YYYY-MM-DD, so plain string sorting is
    # already chronological — reverse=True flips it to newest-first.
    posts.sort(key=lambda p: p["date"], reverse=True)

    # Now write each post, appending its generated ending (newsletter,
    # tag links, share row, previous/next navigation) just before the
    # footer. posts[i-1] is the NEWER neighbour ("next"), posts[i+1]
    # the OLDER one ("previous"), because the list is newest-first.
    for i, post in enumerate(posts):
        next_post = posts[i - 1] if i > 0 else None
        prev_post = posts[i + 1] if i + 1 < len(posts) else None
        ending = build_post_ending_html(post, prev_post, next_post,
                                        newsletter_html)
        page_html = post.pop("page_html")
        page_html = page_html.replace(FOOTER_PLACEHOLDER,
                                      ending + FOOTER_PLACEHOLDER)
        final_html = inject_partials(page_html, nav_html, footer_html,
                                     contact_links_html, newsletter_html)
        write_file(os.path.join(POSTS_OUT_DIR, post["slug"] + ".html"),
                   final_html)

    post_list_html = build_post_list_html(posts)
    tag_filters_html = build_tag_filters_html(posts)

    # 4/6. Build every page, injecting the post list + filter row where
    #    the placeholders exist (only index.html has them; on other pages
    #    replace() simply finds nothing and changes nothing).
    for filename in os.listdir(PAGES_DIR):
        if not filename.endswith(".html"):
            continue
        raw = read_file(os.path.join(PAGES_DIR, filename))
        final_html = inject_partials(raw, nav_html, footer_html, contact_links_html, newsletter_html)
        final_html = final_html.replace(POST_LIST_PLACEHOLDER, post_list_html)
        final_html = final_html.replace(TAG_FILTERS_PLACEHOLDER, tag_filters_html)
        write_file(os.path.join(DOCS, filename), final_html)

    # 5. posts-index.json: the same metadata the homepage list was built
    #    from, as JSON. indent=2 keeps it human-readable in repo diffs.
    index_data = [
        {
            "title": p["title"],
            "date": p["date"],
            "tags": p["tags"],
            "url": f"/posts/{p['slug']}.html",
            "excerpt": p["excerpt"],
        }
        for p in posts
    ]
    write_file(os.path.join(DOCS, "posts-index.json"),
               json.dumps(index_data, indent=2) + "\n")

    # 7. Copy static assets across untouched.
    shutil.copy(os.path.join(SRC, "style.css"), os.path.join(DOCS, "style.css"))
    shutil.copy(os.path.join(SRC, "script.js"), os.path.join(DOCS, "script.js"))

    if os.path.isdir(IMAGES_DIR):
        shutil.copytree(IMAGES_DIR, os.path.join(DOCS, "images"))

    # CNAME must be re-copied on every run (docs/ was wiped in step 1) or
    # GitHub Pages would silently lose the custom domain.
    cname_path = os.path.join(ROOT, "CNAME")
    if os.path.exists(cname_path):
        shutil.copy(cname_path, os.path.join(DOCS, "CNAME"))

    print(f"Built {len(os.listdir(PAGES_DIR))} pages and {len(posts)} posts into docs/")


if __name__ == "__main__":
    build()
