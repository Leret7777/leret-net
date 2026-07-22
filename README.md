# leret.me

Personal site for Leret. The **homepage** is a single, no-scroll hero: the
**LERET** wordmark and tagline on the left, a rotated "paper pile" of the
three newest posts on the right, and a contact strip below. **See all
posts →** opens a full-screen overlay listing every post. Each post has
its **own reading page** (a shareable permalink) with a meta row, optional
hero image, and a subscribe box. There's also a standalone **About** page.

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
  pages/       standalone pages:
                 index.html   the homepage (wordmark hero + paper pile +
                              contact strip + the All-Posts overlay markup)
                 about.html   bio + modelling representation
  partials/    shared markup injected into every page by build.py:
                 nav.html      just the round theme toggle (top-right)
                 footer.html   currently empty (kept as an injection point)
  posts/       one .html file per post — ALL content lives here.
                 _TEMPLATE.html    commented starter (ignored by build)
  images/      site images:
                 profile/          portrait art
                 modeling/<shoot>/ modelling gallery photos
  style.css    the one shared stylesheet (dark default + light theme)
  script.js    theme toggle, All-Posts overlay, search + tag filtering,
               reading progress, photo lightbox

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
3. Builds the homepage **paper pile** from the three newest posts (each a
   rotated "polaroid" card linking to its page) and the **All-Posts
   overlay grid** from every post, and injects both into `index.html`.
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
  shown as the post's **category** in the meta row and overlay card.
- `excerpt` — optional one-line teaser.
- `image` — optional. A path like `/images/my-hero.jpg`. When set, it
  becomes the post's hero image, the polaroid photo on the homepage, and
  the tile in the All-Posts overlay. Leave it empty and those fall back
  to a neutral placeholder tile.

The rest of the file is normal HTML; write the article inside `<main>`.
The quickest start is to **copy `src/posts/_TEMPLATE.html`**.

Run `python3 build.py` and the post appears in the paper pile (if it's
one of the three newest) and the All-Posts overlay, with its reading
time, category, subscribe box, and reading page — all added
automatically.

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

The polaroid cards use a warm paper tone (`#f5f0e4`) in both themes.

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
- **All-Posts overlay** — **See all posts →** fades in a full-screen
  panel listing every post; closes on the ✕, a backdrop click, or
  Escape. It's a normal DOM element in `index.html` toggled by the
  `.is-open` class — not a separate page.
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

- The homepage **contact strip** has the email (Bungee), Instagram /
  LinkedIn links, and a "Comp card" mailto. The Instagram/LinkedIn links
  currently point at `#` — put your real URLs into `src/pages/index.html`.
- Modelling bookings live on the **About page**: Brother Models,
  Francesca's email, and "Request comp card" / "Request digitals"
  buttons.
- The Subscribe box on each post uses Formspree — replace
  `REPLACE_WITH_YOUR_FORM_ID` in `build.py` (`build_subscribe_html`) with
  a real form ID from https://formspree.io.

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
