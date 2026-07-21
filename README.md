# leret.me

Personal site for Leret. It's a **single scrolling page**: an intro, a
feed of every post's full content (tagged, filterable), and an About
section (bio + modelling bookings). Each post also has its **own page**
(a permalink you can share) that the feed links to.

Hand-written HTML, CSS, and JavaScript. No static site generator, no
templating engine, no framework. The only "build step" is a small
standard-library-only Python script, `build.py`.

## The 30-second version (how to make a change)

1. Edit files in **`src/`** (never in `docs/`).
2. Run **`python3 build.py`**.
3. Commit **both `src/` and `docs/`**, then push. GitHub Pages serves
   what's in `docs/`.

To write a new post: copy `src/posts/_TEMPLATE.html`, follow the
checklist inside it, and run the build. Every post file also has a
"HOW TO EDIT THIS POST" comment at the top.

## How this is structured

```
src/
  pages/       standalone pages: index.html — the whole one-page site
               (intro + post feed + About section)
  partials/    shared markup injected into every page by build.py:
                 nav.html          header (logo, search, Posts, About,
                                   contact icons, theme toggle)
                 footer.html       the copyright line
                 contact-links.html  the Instagram / LinkedIn / email
                                   icons (used in the header and at the
                                   bottom of each post)
                 newsletter.html   the email signup box (About page +
                                   the end of each post)
  posts/       one .html file per post — ALL content lives here.
                 _TEMPLATE.html    commented starter (ignored by build)
  images/      site images:
                 profile/          homepage portrait + About portrait
                 modeling/<shoot>/ modelling gallery photos
  style.css    the one shared stylesheet (light + dark themes)
  script.js    theme toggle, search + tag filtering, reading progress,
               photo lightbox

scripts/
  resize_images.py   optional Pillow helper: shrinks/compresses raw
                     photos from incoming/ into src/images/

incoming/      drop raw, full-size photos here before resizing
               (gitignored — never committed)

build.py       reads src/ and writes the finished site into docs/
docs/          what GitHub Pages serves. GENERATED — never hand-edit.
CNAME          "leret.me" — copied into docs/ on every build.
```

## What `build.py` does

Run it after any change in `src/`:

```
python3 build.py
```

Standard library only — nothing to install. It:

1. Wipes and recreates `docs/`.
2. Reads each post in `src/posts/` (files starting with `_` are
   skipped, e.g. the template), parses its metadata comment, works out
   its reading time, injects the shared nav/footer + a generated ending
   (newsletter, tags, share links, previous/next), and writes it to
   `docs/posts/`.
3. Generates the homepage post list (newest first, with tag labels,
   excerpts, and reading time) and the tag filter row, and injects them
   into `index.html`.
4. Writes `docs/posts-index.json` (title/date/tags/url/excerpt/reading
   time for every post).
5. Copies `style.css`, `script.js`, `images/`, and `CNAME` into `docs/`.

## Adding or editing a post

Every post is one file in `src/posts/`. The **first line** is its
settings, fields separated by `|`:

```html
<!-- title: My New Post | date: 2026-08-01 | tags: commercial | excerpt: One short line shown on the homepage. -->
```

- `title` and `date` (YYYY-MM-DD) are required. `date` sets the order on
  the homepage.
- `tags` — one per post: `commercial` or `modelling`. (The build
  supports several comma-separated, or none, but warns if a post doesn't
  have exactly one.)
- `excerpt` — optional one-line teaser for the homepage list.

The rest of the file is normal HTML; write the article inside `<main>`.
The quickest start is to **copy `src/posts/_TEMPLATE.html`** — it has a
step-by-step checklist and every post already carries a "HOW TO EDIT
THIS POST" comment pointing at these same things.

Run `python3 build.py` and the post appears on the homepage with its
reading time, tag, share links, newsletter, and previous/next links —
all added automatically.

## Tags

The tag filter row on the homepage is **derived from the posts** at
build time — whatever `tags:` values exist become filter buttons.
Right now that's `commercial` and `modelling`; writing `tags: book` on a
future post would add a "Book" button on the next build, no code change.
A link like `/?tag=modelling` opens the homepage pre-filtered.

## Photos

**Profile picture** — the big portrait on the left of the one-page site
is a placeholder SVG in `src/images/profile/`. To use a real photo:

1. Shrink it with the resize script (below) into `src/images/profile/`.
2. Point the `.home-split__photo img` `src` in `src/pages/index.html`
   at it (e.g. `portrait.jpg`).
3. `python3 build.py`.

**Modelling gallery photos** — in `src/posts/modelling-portfolio.html`
(look for the "ADD GALLERY PHOTOS HERE" comment):

1. Drop raw photos into `incoming/<something>/` (gitignored).
2. Resize into place (needs `pip install Pillow`, the one external
   dependency, isolated to this script):

   ```
   python3 scripts/resize_images.py incoming/<something> src/images/modeling/<shoot>
   ```

3. Copy a `<button class="gallery__item">…</button>` block per photo and
   point its `src`/`data-full` at the new files.
4. `python3 build.py`.

**A photo inside any post** — put the file in `src/images/`, then add
`<img src="/images/my-photo.jpg" alt="description">` wherever you want
it inside `<main>`.

## Embedding a video

Inside a post, wrap the platform's embed URL in the 16:9 container:

```html
<div class="video-embed">
  <iframe src="https://www.youtube.com/embed/VIDEO_ID" ...></iframe>
</div>
```

No video files are stored in the repo — always a hosted embed.

## Features in `script.js`

- **Search** — the header magnifying glass reveals an input; typing
  filters the homepage list live (Escape clears + closes). On other
  pages, Enter jumps to the homepage with the query (`/?q=...`).
- **Tag filtering** — clicking a tag pill narrows the list. Search and
  tags share one function: a post must match both to stay visible.
- **Theme** — light/dark via CSS custom properties; follows the OS by
  default, the header toggle overrides and remembers the choice in
  `localStorage`. No pure black/white anywhere.
- **Reading time** — `· N min read` shown on the homepage list and each
  post header. build.py counts words in the post's `<main>` (~200 wpm);
  fully automatic.
- **Reading progress** — a thin accent bar fills across the top of a
  post as you scroll.
- **Lightbox** — click a gallery photo to enlarge it.

## One-page layout

The whole site is one scrolling page (`src/pages/index.html`): a
full-height portrait sticks in place (`position: sticky`) on the left
while the right side scrolls through the intro, the full-text post feed,
and the About section (~40/60, stacks to one column on mobile). The
header's **Posts** / **About** links jump to the `#posts` / `#about`
sections (written `/#…` so they also work from a standalone post page).

`build.py` inlines each post's full `<main>` content into the feed as a
filterable article whose heading links to that post's own page — so the
post exists both in the feed and at its own shareable URL. The shared
lightbox lives at the bottom of `index.html` so the inlined modelling
gallery works.

## Contact & bookings

- Contact icons (Instagram / LinkedIn / email) live in the **header** on
  every page, and at the end of every post. They currently point at `#`
  — put your real Instagram/LinkedIn URLs into
  `src/partials/contact-links.html` (one file updates them everywhere).
- Modelling bookings live in the **About section** of the one page:
  Brother Models, Francesca's email, and "Request comp card" / "Request
  digitals" buttons.
- The newsletter Subscribe button and any Formspree-based form need a
  real form ID from https://formspree.io in place of
  `REPLACE_WITH_YOUR_FORM_ID`.

## GitHub Pages settings

Settings → Pages: **Deploy from a branch**, branch `main`, folder
`/docs`. Custom domain `leret.me`, "Enforce HTTPS" ticked once the
certificate is issued.

## Custom domain (leret.me) — DNS records

At the registrar for `leret.me`:

| Type  | Name | Value               |
|-------|------|---------------------|
| A     | @    | 185.199.108.153     |
| A     | @    | 185.199.109.153     |
| A     | @    | 185.199.110.153     |
| A     | @    | 185.199.111.153     |
| CNAME | www  | leret7777.github.io |

The root `CNAME` file (just `leret.me`) tells Pages which domain to
serve; build.py copies it into `docs/` on every run.

## Design notes

- Calm, muted sage/forest green as the single accent; softened neutrals
  (no `#000`/`#fff`). Serif headings, native UI font for body.
- Tag labels and filter pills are deliberately quiet — metadata, not the
  focus.
- The contact/share icons are **inline SVGs** using
  `stroke="currentColor"`, so the CSS color rules (and the theme toggle)
  recolor them with no extra code — no icon font, no CDN.
- `script.js` and `style.css` are commented section by section; read
  them together.
