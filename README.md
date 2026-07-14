# leret.me

Personal site for Leret — commercial/data work portfolio, modeling
portfolio, writing, a book-in-progress, and (eventually) a shop.

Hand-written HTML, CSS, and JavaScript. No static site generator, no
templating engine, no frontend framework. The only "build step" is a
small standard-library-only Python script, `build.py`, that stitches the
shared nav/footer into every page and auto-generates the Writing listing.

## How this is structured

```
src/
  pages/       one real, complete .html file per top-level section
               (index, work, modeling, writing, book, shop, about)
  partials/    nav.html and footer.html — shared header/footer markup
  posts/       one .html file per blog post / article
  images/      site images, organized by section (e.g. images/modeling/<shoot>/)
  style.css    the one shared stylesheet
  script.js    the one script — the modeling gallery lightbox

scripts/
  resize_images.py   optional Pillow-based helper: shrinks/compresses
                      raw photos from incoming/ into src/images/

incoming/      drop raw, full-size photos here before resizing.
               Gitignored — nothing in here ever gets committed.

build.py       reads everything in src/ and writes the finished site
               into docs/

docs/          the actual folder GitHub Pages serves. Fully generated —
               don't hand-edit anything in here, it gets wiped and
               rebuilt every time you run build.py.

CNAME          contains "leret.me" — copied into docs/ on every build
               so GitHub Pages keeps serving the custom domain.
```

## Running the build

Whenever you change anything in `src/` (or `CNAME`), regenerate `docs/`:

```
python3 build.py
```

This is standard-library-only — nothing to install. It will:

1. Wipe and recreate `docs/` from scratch.
2. Read `src/partials/nav.html` and `src/partials/footer.html`.
3. Build every post in `src/posts/` first (parsing its metadata comment,
   injecting nav/footer, writing it to `docs/posts/`), collecting
   title/date/slug for each.
4. Build every page in `src/pages/` (injecting nav/footer, and — on
   `writing.html` only — the auto-generated post list, sorted newest
   first).
5. Copy `src/style.css`, `src/script.js`, `src/images/`, and `CNAME` into
   `docs/`.

Then commit **both** `src/` and the regenerated `docs/`, and push:

```
git add src build.py docs CNAME
git commit -m "..."
git push
```

There's no CI and no GitHub Actions — `docs/` in the repo *is* what gets
served, so it has to be committed, not just generated locally.

## Adding a blog post / article

1. Create a new file in `src/posts/`, e.g. `src/posts/my-new-post.html`.
2. Start it with a metadata comment giving the title and date:

   ```html
   <!-- POST META
   title: My New Post
   date: 2026-03-01
   -->
   <!DOCTYPE html>
   <html lang="en">
   ...
   ```

3. Write the rest as a normal complete page — `<head>` with its own
   `<title>`/meta description, `<!-- NAV -->` and `<!-- FOOTER -->`
   placeholders, and your content inside `<main>`. Copy the structure of
   an existing post in `src/posts/` as a starting point.
4. Run `python3 build.py`. The post is written to `docs/posts/`, and it
   automatically appears in the Writing page listing — you never edit
   `writing.html` by hand for this.

## Adding modeling photos

1. Drop the raw, full-size photos into `incoming/<something>/` (any
   subfolder name — it's gitignored, so organize it however's convenient
   for yourself).
2. Resize and compress them into the right place in `src/images/`:

   ```
   python3 scripts/resize_images.py incoming/<something> src/images/modeling/<shoot-or-category>
   ```

   This requires Pillow (`pip install Pillow`) — the one external
   dependency in the whole project, and it's isolated to this one script.
   It resizes each photo so its longest edge is at most 1600px and
   re-saves it as a compressed JPEG, so the repo doesn't fill up with
   multi-megabyte camera originals.
3. Add `<button class="gallery__item"><img src="..." data-full="..."
   alt="..."></button>` entries in `src/pages/modeling.html` pointing at
   the new files (copy an existing gallery item as a template).
4. Run `python3 build.py`.

## Embedding a new video

In `src/pages/modeling.html`, the video reel is a responsive wrapper
around an `<iframe>`:

```html
<div class="video-embed">
  <iframe src="https://www.youtube.com/embed/VIDEO_ID" ...></iframe>
</div>
```

Replace the `src` with the embed URL for a YouTube or Vimeo video (use
the platform's own "Share → Embed" link to get the correct `/embed/...`
URL). No video files are ever stored in this repo — it's always a
hosted embed.

## GitHub Pages settings

In the repo's Settings → Pages:

- **Source:** Deploy from a branch
- **Branch:** `main`, folder `/docs`

GitHub Pages will then serve whatever is committed in `docs/` on `main`
— which is why `build.py`'s output has to be committed and pushed, not
just generated locally.

## Custom domain (leret.me) — DNS records

At your domain registrar, add these records for `leret.me`:

**Apex domain (`leret.me`) — four A records, all pointing at GitHub
Pages' IPs:**

| Type | Name | Value            |
|------|------|------------------|
| A    | @    | 185.199.108.153  |
| A    | @    | 185.199.109.153  |
| A    | @    | 185.199.110.153  |
| A    | @    | 185.199.111.153  |

(Optional but recommended — IPv6 equivalents:)

| Type | Name | Value                   |
|------|------|-------------------------|
| AAAA | @    | 2606:50c0:8000::153     |
| AAAA | @    | 2606:50c0:8001::153     |
| AAAA | @    | 2606:50c0:8002::153     |
| AAAA | @    | 2606:50c0:8003::153     |

**`www` subdomain — one CNAME record, so `www.leret.me` also resolves:**

| Type  | Name | Value                  |
|-------|------|------------------------|
| CNAME | www  | leret7777.github.io    |

After adding these (DNS propagation can take up to a few hours), go back
to Settings → Pages, enter `leret.me` as the custom domain, and once
GitHub verifies it, enable "Enforce HTTPS".

The `CNAME` file at the repo root (containing just `leret.me`) is what
tells GitHub Pages which custom domain to serve — `build.py` copies it
into `docs/` on every run so it can't accidentally get lost when `docs/`
is rebuilt.

## Design notes

- One shared stylesheet (`src/style.css`), one accent color (terracotta),
  a serif for headings and the OS's native UI font for body text — no
  external font downloads.
- The mobile nav menu uses a pure-CSS "checkbox hack" (a hidden checkbox
  + a styled `<label>`), so it needs zero JavaScript.
- The only real JavaScript is `src/script.js`, which powers the modeling
  gallery's click-to-enlarge lightbox. It's commented in detail — read it
  alongside the `.gallery`/`.lightbox` rules in `style.css` to see how the
  two work together.
