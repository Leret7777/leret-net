# How leret.me should feel

This is the design direction the site agent works towards. It was written
from three sites Leret said "speak to him", and from the design choices he
has already made. The agent changes the site **towards** this, one small
step a day, using the roadmap at the bottom.

## The feeling, in one sentence

A warm, personal home on the internet for someone who works in two lanes,
commercial data and AI automation by day and modelling by night, that
feels human, shows the work, and makes it easy to get in touch.

## What Leret liked in each reference

**careerhannah.com: "many lanes, one person"**
- A big, confident name at the top, with a short line of who she is
  across several roles.
- A real photo of her near the top, captioned with a place and date.
- Clear sections down the page (her work, her audience, speaking,
  writing, contact), each with a short heading where one or two words
  are set in *italics* for emphasis.
- Numbered items (01, 02, 03) for lists of topics and ways to work
  together.
- Contact split by reason (partnerships, press, speaking, everything
  else), each with its own pre-filled email.

**pawlean.com: "a blog that is a home"**
- Opens with a friendly first-person hello and a short paragraph:
  who she is, where she's based, what she writes about, with the topic
  words themselves being links.
- A few pinned posts, then a "Latest" list of titles with dates.
- Things posted elsewhere (YouTube, etc.) sit in the same list, marked
  with a small arrow so you know they open another site.
- A simple top menu of a handful of words.
- A "Looking for more?" list of everywhere else to find her.
- Proudly British in tone.

**sophiejouvenaar.com: "let the photos talk"**
- The photography is the page: a grid of images, almost no text.
- Work grouped into a few clear collections in the menu.
- Very quiet design so nothing competes with the pictures.

## What stays fixed (do not change)

- **Colours**: the existing forest-green palette in `src/style.css`
  (dark default, light theme, no pure black or white).
- **Fonts**: Bungee only for the LERET wordmark and contact email;
  Public Sans for body and headings; IBM Plex Mono for small labels,
  dates and numbers.
- The theme toggle, and the build process (`src/` → `build.py` → `docs/`).
- Two categories of post: `commercial` and `modelling`.

## Voice

First person, warm, plain British English. Short sentences. No jargon
without explaining it. Confident but not salesy. Northern warmth is
welcome (he's in Manchester). Never sound like marketing copy.

## Design roadmap (do these in order, one per run)

Tick an item (`[x]`) when it's done, and note it in the log. Skip an item
that is blocked on something only Leret can provide (a photo, a link):
add the blocker to `agent/NEEDS_FROM_LERET.md` and move to the next item.

- [x] 1. **Friendly intro on the homepage.** Under the wordmark, replace
      the one-line tagline with a short first-person hello (2 to 3
      sentences): who he is, Manchester, the two lanes, with
      "commercial" and "modelling" linking to those post lists. Use only
      facts from `agent/SOURCES.md`.
- [x] 2. **Simple top menu.** A small row of mono links next to the theme
      toggle: Writing, Modelling, About, Contact. Works on phones.
- [ ] 3. **Section headings with an italic accent.** Give each homepage
      section a short heading where one or two words are in italics
      (e.g. "Latest *writing.*"). Add the small CSS for it.
- [ ] 4. **Pinned posts.** Let a post be pinned with `pinned: yes` in its
      first-line settings; show up to 3 pinned posts above "Latest" on the
      homepage. (This needs a small change to how the homepage list is
      made; do it inside `src/` and the page templates if possible,
      otherwise add it to NEEDS as a build change for Leret to approve.)
- [ ] 5. **Modelling grid.** Turn the modelling portfolio into a
      photo-first grid with minimal text, using the existing lightbox.
      Blocked until real photos exist.
- [ ] 6. **Photo of Leret near the top of the homepage**, captioned with
      place and month/year. Blocked until a real photo exists.
- [ ] 7. **Contact by reason.** Numbered contact options: 01 Modelling
      bookings (to his agent Francesca, as on the About page), 02
      Speaking and community, 03 Everything else (to Leret). Each a
      pre-filled email.
- [ ] 8. **"Find me elsewhere" list** at the bottom of the homepage, only
      with links that are filled in `agent/SOURCES.md`.
- [ ] 9. **Posts from elsewhere** (Substack, YouTube) shown in the post
      list with a small ↗ marker.
- [ ] 10. **Polish pass.** Check spacing, phone layout, both themes, and
      page speed. Fix small things only.

When every item is ticked, design work is limited to small fixes and
consistency; never start a redesign on your own.
