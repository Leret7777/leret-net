# leret.me

Personal site for Leret. Everything on it is a **post** — work,
modeling, book updates, general writing — categorized by tags and
listed chronologically on the homepage.

Hand-written HTML, CSS, and JavaScript. No static site generator, no
templating engine, no frontend framework. The only "build step" is a
small standard-library-only Python script, `build.py`, that stitches
the shared nav/footer into every page and generates the homepage post
list, the tag filter row, and a JSON index of all posts.

## How this is structured

```
src/
  pages/       standalone pages: index.html (the homepage) and
               about.html. Adding e.g. a Shop page later is just a new
               file here plus a header link.
  partials/    nav.html and footer.html — shared header/footer markup,
               injected into every page by build.py. The footer holds
               ALL contact info (email, socials, Brother Models comp
               card request), so it's visible from every page.
  posts/       one .html file per post — every piece of content on the
               site lives here, tagged via its metadata comment
  images/      site images (e.g. images/modeling/<shoot>/)
  style.css    the one shared stylesheet (light + dark themes)
  script.js    the one script: theme toggle, tag/search filtering,
               photo lightbox

scripts/
  resize_images.py   optional Pillow-based helper: shrinks/compresses
                      raw photos from incoming/ into src/images/

incoming/      drop raw, full-size photos here before resizing.
               Gitignored — nothing in here ever gets committed.

build.py       reads everything in src/ and writes the finished site
               into docs/

docs/          the folder GitHub Pages serves. Fully generated — don't
               hand-edit anything in here, it's wiped and rebuilt on
               every run of build.py.

CNAME          contains "leret.me" — copied into docs/ on every build
               so GitHub Pages keeps serving the custom domain.
```

## Running the build

Whenever you change anything in `src/` (or `CNAME`):

```
python3 build.py
```

Standard library only — nothing to install. It will:

1. Wipe and recreate `docs/` from scratch.
2. Read the two shared partials (nav, footer).
3. Build every post in `src/posts/` (parse its metadata comment, inject
   nav/footer, write it to `docs/posts/`).
4. Generate the homepage post list (newest first, with tag labels and
   excerpts) and the tag filter row, injected into `index.html` at the
   `<!-- POST_LIST -->` and `<!-- TAG_FILTERS -->` placeholders.
5. Write `docs/posts-index.json` — every post's title/date/tags/url/
   excerpt as machine-readable JSON.
6. Copy `style.css`, `script.js`, `images/`, and `CNAME` into `docs/`.

Then commit **both** `src/` and the regenerated `docs/`, and push:

```
git add src build.py docs CNAME
git commit -m "..."
git push
```

There's no CI — `docs/` in the repo *is* what gets served.

## Adding a post

1. Create a new file in `src/posts/`, e.g. `src/posts/my-new-post.html`.
2. The **first line** is a single-line metadata comment, fields
   separated by `|`:

   ```html
   <!-- title: My New Post | date: 2026-08-01 | tags: work | excerpt: One short line shown on the homepage. -->
   ```

   - `title` and `date` (YYYY-MM-DD) are required.
   - `tags` is optional — comma-separate for more than one
     (`tags: modeling, work`), or leave the field out entirely for an
     untagged post.
   - `excerpt` is optional — it's the one-liner under the title in the
     homepage list.

3. The rest of the file is a normal complete page — copy an existing
   post in `src/posts/` as a starting point (head with its own
   `<title>`/meta description, `<!-- NAV -->` / `<!-- FOOTER -->`
   placeholders, content inside `<main>`).
4. Run `python3 build.py`. The post appears on the homepage
   automatically, and its tags join the filter row — nothing else to
   edit.

## Tags

The tag filter row on the homepage is **derived from the posts
themselves** at build time — whatever tags exist across all posts become
filter buttons. Using a brand-new tag in one post's metadata is all it
takes to add a category to the site.

Current convention: `work` (commercial/data), `modeling`, `book`,
`writing` (general articles) — but nothing enforces this list.

## Search, tag filtering, and themes (script.js)

- **Search**: the header search box filters the homepage list as you
  type. On any other page, pressing Enter jumps to the homepage with
  the query applied (`/?q=...`). `/?tag=...` works the same way for tags.
- **Tag filtering**: clicking a tag pill narrows the list to that tag.
  Search and tag filter share one function — a post must match *both*
  to stay visible.
- **Theme**: colors are CSS custom properties in two sets (light/dark).
  Default follows the visitor's OS preference; the header toggle
  overrides it and remembers the choice in `localStorage`. No pure
  black or pure white anywhere — soft paper tones in light mode, soft
  charcoal in dark.

## Adding modeling photos

1. Drop raw photos into `incoming/<something>/` (gitignored).
2. Resize/compress into place (needs `pip install Pillow` — the one
   external dependency, isolated to this script):

   ```
   python3 scripts/resize_images.py incoming/<something> src/images/modeling/<shoot-or-category>
   ```

3. Add `<button class="gallery__item"><img src="..." data-full="..."
   alt="..."></button>` entries in the relevant modeling post (copy an
   existing gallery item), keeping the `<div class="lightbox">` block at
   the bottom of the post.
4. Run `python3 build.py`.

## Embedding a video

Inside a post, wrap the platform's embed URL in the responsive 16:9
container:

```html
<div class="video-embed">
  <iframe src="https://www.youtube.com/embed/VIDEO_ID" ...></iframe>
</div>
```

No video files are stored in the repo — always a hosted embed.

## GitHub Pages settings

Settings → Pages: **Deploy from a branch**, branch `main`, folder
`/docs`. Custom domain: `leret.me`, with "Enforce HTTPS" ticked once
the certificate is issued.

## Custom domain (leret.me) — DNS records

At the domain registrar for `leret.me`:

| Type | Name | Value            |
|------|------|------------------|
| A    | @    | 185.199.108.153  |
| A    | @    | 185.199.109.153  |
| A    | @    | 185.199.110.153  |
| A    | @    | 185.199.111.153  |
| CNAME | www | leret7777.github.io |

The `CNAME` file at the repo root (containing just `leret.me`) tells
GitHub Pages which domain to serve — `build.py` copies it into `docs/`
on every run so it can't get lost when `docs/` is rebuilt.

## Design notes

- Calm, muted sage/forest green as the single accent; softened neutrals
  (no `#000`/`#fff` anywhere). Serif headings, native UI font for body.
- Tag labels and filter pills are deliberately quiet — they're metadata,
  not the focus.
- The lightbox and the filtering logic in `script.js` are commented in
  detail — read them alongside the matching sections of `style.css`.
