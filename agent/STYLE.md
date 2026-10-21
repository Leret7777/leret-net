# How leret.me should feel

This is the design direction the site agent works towards. **Rewritten
21 Oct 2026**: Leret found the site too busy and asked for it to be clean
and streamlined, like sophiejouvenaar.com, with photos on the page as
soon as it opens.

## The feeling, in one sentence

Quiet and picture-led: Leret's photos do most of the talking, with a few
calm words alongside about who Leret is, what Leret writes, and how to
get in touch.

## The homepage layout (keep it)

Two sides, nothing else:

- **Left: words.** The LERET wordmark, a small menu (Writing, Modelling,
  About), one short paragraph, the three newest post titles with month
  and year, and contact details. On tall screens it stays still while
  the photos scroll.
- **Right: photos.** A two-column wall of photos, square corners, tight
  gaps, no captions on the wall. Clicking a photo opens it larger.
- **No bar, menu pill or floating button on top of the homepage.**
- On phones: intro first, then the photos, then writing and contact.

## Rules that keep it clean

- Add photos, not sections. New photos Leret approves go on the photo
  wall (newest shoot first) and/or in the relevant post. Never add new
  blocks, lists, banners or headings to the homepage.
- No italic-accent headings, no numbered lists (01, 02, 03) unless it's
  a real sequence, no small all-caps labels, no "Find me elsewhere"
  blocks, no arrows on links.
- Keep words short. If something new needs saying, it goes in a post,
  not on the homepage.
- Credit photographers under the photos (as with "Polaroids: Brother
  Models").

## What stays fixed (do not change)

- **Colours**: the existing forest-green palette in `src/style.css`
  (dark default, light theme, no pure black or white).
- **Fonts**: Bungee only for the LERET wordmark; Public Sans for
  everything else on the homepage.
- The build process (`src/` → `build.py` → `docs/`).
- Two categories of post: `commercial` and `modelling`.

## Voice

First person, warm, plain British English. Short sentences. No jargon
without explaining it. Never sound like marketing copy.

## Design roadmap (do these in order, one per run)

Tick an item (`[x]`) when it's done, and note it in the log. Skip an item
that is blocked on something only Leret can provide: add the blocker to
`agent/NEEDS_FROM_LERET.md` and move to the next item.

- [x] 1. **Split homepage**: words left, photos right (done by hand,
      21 Oct 2026).
- [ ] 2. **Calm the other pages to match.** On the About page, the
      Writing (all posts) page and the post pages: remove clutter in the
      same spirit (no italic-accent headings, no extra label rows), keep
      the content. Small, careful changes, one page per run.
- [ ] 3. **New photos onto the wall.** When the Sophie test shoot or
      Manchester Fashion Week photos arrive, add the best few to the top
      of the homepage photo wall, credited, as well as to their posts.
- [ ] 4. **Polish pass.** Check spacing, phone layout, both themes, and
      page speed. Fix small things only.

When every item is ticked, design work is limited to small fixes and
consistency; never start a redesign on your own.
