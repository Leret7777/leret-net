# leret.me

Personal site for Leret. The **homepage** is a centered **LERET** wordmark
and tagline, then the **newest few posts** as a reading list (mono title,
date + read time, excerpt) with an **All Posts →** link to the full list
(`/all-posts.html`). Each post has its **own reading page** (a shareable
permalink) with a meta row, optional hero image, and a subscribe box.
There's also a standalone **About** page.

Hand-written HTML, CSS, and JavaScript. No static site generator, no
templating engine, no framework. The only "build step" is a small
standard-library-only Python script, `build.py`.

## The site agent (runs every morning)

A Claude agent looks after this site daily, on its own, via
`.github/workflows/site-agent.yml`. Each run it checks for broken
things, turns anything in `inbox/` into posts or updates, pulls in new
material from the sources in `agent/SOURCES.md`, and makes one small
design step towards `agent/STYLE.md`. A safety check (`agent/guard.py`)
then undoes anything it wasn't allowed to touch and makes sure the site
still builds before publishing.

- **What it did:** a "Site agent report" issue appears on GitHub after
  every run (you get a notification), and the full history is in
  `agent/LOG.md`
- **Undo:** reply to that day's report with `undo` (everything from that
  day) or say in words what to undo (just that part). Undone things are
  recorded in `agent/FEEDBACK.md` so the agent doesn't repeat them.
- **What it needs from you:** `agent/NEEDS_FROM_LERET.md`
- **Its job description:** `agent/BRIEF.md`
- **Give it material:** drop notes or photos in `inbox/`

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
  pages/       standalone pages:
                 index.html     the homepage (wordmark header + newest
                                posts + All Posts link + contact strip)
                 all-posts.html the full reading list of every post
                 about.html     bio + modelling representation
  partials/    shared markup injected into every page by build.py:
                 nav.html      just the round theme toggle (top-right)
                 footer.html   currently empty (kept as an injection point)
  posts/       one .html file per post — ALL content lives here.
                 _TEMPLATE.html    commented starter (ignored by build)
  images/      site images:
                 profile/          portrait art
                 modeling/<shoot>/ modelling gallery photos
  style.css    the one shared stylesheet (dark default + light theme)
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
   its reading time, and rewrites it as a **reading page**: a `← Back`
   link, a meta row (`category · N min read · date`), an optional hero
   image after the title, and a subscribe box before the footer.
3. Builds the **post reading list** (mono title, calendar date + read
   time, excerpt) — the newest few into `index.html`, and every post into
   `all-posts.html`. The homepage limit is `HOME_FEED_LIMIT` in
   `build.py`.
4. Writes `docs/posts-index.json` (title/date/tags/category/url/excerpt/
   image/reading time for every post).
5. Copies `style.css`, `script.js`, `images/`, and `CNAME` into `docs/`.

## Adding or editing a post

Every post is one file in `src/posts/`. The **first line** is its
settings, fields separated by `|`:

```html
<!-- title: My New Post | date: 2026-08-01 | tags: commercial | excerpt: One short line. | image: /images/my-hero.jpg -->
```

- `title` and `date` (YYYY-MM-DD) are required. `date` sets the order
  everywhere (newest first).
- `tags` — one per post: `commercial` or `modelling`. The first tag is
  shown as the post's **category** in the feed card and meta row.
- `excerpt` — optional one-line teaser.
- `image` — optional. A path like `/images/my-hero.jpg`. When set, it
  becomes the post's hero image on its reading page. Leave it empty and
  the reading page simply has no hero. (The homepage feed cards are
  text-only — no image.)

The rest of the file is normal HTML; write the article inside `<main>`.
The quickest start is to **copy `src/posts/_TEMPLATE.html`**.

Run `python3 build.py` and the post appears in the homepage feed with its
category, reading time, and date, plus its own reading page (subscribe
box included) — all added automatically.

## The design system

**Palette** (dark is the default; light is a full theme, no pure
black/white anywhere):

| Role          | Dark      | Light     |
|---------------|-----------|-----------|
| Background    | `#1c211c` | `#eeeae0` |
| Text          | `#ebe8df` | `#2a2f27` |
| Muted text    | `#b0aca2` | `#5f6459` |
| Surface       | `#252a25` | `#e4dfd2` |
| Border        | `#3a4239` | `#c9c4b5` |
| Accent        | `#8fbc95` | `#3a6d4a` |

Post cards sit on the surface tone with a border that turns accent on
hover.

**Fonts** (Google Fonts, loaded via one `@import` at the top of
`style.css`):

- **Bungee** — the display face. Used *only* for the `LERET` wordmark and
  the contact email. Deliberately loud, so it's rationed.
- **Public Sans** — all body text and headings.
- **IBM Plex Mono** — small labels, eyebrows, and post meta.

**Theme toggle** — the round button top-right (from `nav.html`). Dark is
the default; the toggle overrides and remembers the choice in
`localStorage`.

## Features in `script.js`

- **Theme** — dark/light via CSS custom properties. Dark by default;
  the top-right toggle flips it and persists the choice in `localStorage`.
- **Search + tag filtering** — retained from before; filters lists live.
- **Reading time** — `N min read` in each post's meta row. build.py
  counts words in the post's `<main>` (~200 wpm); fully automatic.
- **Reading progress** — a thin accent bar fills across the top of a
  post as you scroll.
- **Lightbox** — click a gallery photo to enlarge it.

## Photos

Set a post's hero/thumbnail with the `image:` metadata field (see
"Adding or editing a post"). To shrink raw photos first:

1. Drop raw photos into `incoming/<something>/` (gitignored).
2. Resize into place (needs `pip install Pillow`, the one external
   dependency, isolated to this script):

   ```
   python3 scripts/resize_images.py incoming/<something> src/images/modeling/<shoot>
   ```

3. Point the post's `image:` field (or an inline `<img>` in `<main>`) at
   the new file, then `python3 build.py`.

## Embedding a video

Inside a post, wrap the platform's embed URL in the 16:9 container:

```html
<div class="video-embed">
  <iframe src="https://www.youtube.com/embed/VIDEO_ID" ...></iframe>
</div>
```

No video files are stored in the repo — always a hosted embed.

## Contact & bookings

- The homepage **contact strip** has the email (Bungee) and Instagram /
  LinkedIn / Substack links (the same links are listed in
  `agent/SOURCES.md`, which the site agent works from).
- Modelling bookings live on the **About page**: Brother Models,
  Francesca's email, and "Request comp card" / "Request digitals"
  buttons.
- The Subscribe box on each post is one button that opens Leret's
  Substack sign-up page (`SUBSTACK_URL` in `build.py`), where readers
  enter their email. No other service needed.

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
