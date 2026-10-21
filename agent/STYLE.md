# How leret.me should feel

This is the design direction the site agent works towards. **Rewritten
21 Oct 2026**: Leret found the site too busy and asked for it to be clean
and streamlined, like sophiejouvenaar.com, with photos on the page as
soon as it opens.

## The feeling, in one sentence

Quiet and picture-led: Leret's photos do most of the talking, with a few
calm words alongside about who Leret is, what Leret writes, and how to
get in touch.

## The layout (keep it): two sides on every page

- **Left: the same column on every page** (`src/partials/nav.html`): the
  LERET wordmark (goes back to the photos), one short paragraph, links
  to About me and Featured in, the list of every post with month and year, and
  contact details. On tall screens it stays still.
- **Right: the page itself.** The photo wall on the homepage; the post,
  the About page or the portfolio everywhere else. Tapping a post title
  on the left opens it on the right.
- **Less navigation.** No menu, no Back links, no "All posts" link, no
  theme button, no reading-progress bar, nothing floating on top. The
  list of posts is the navigation. Light/dark follows the visitor's
  device.
- On phones: LERET at the top, then the page, then the posts list and
  contact at the bottom.
- **Two quiet page links** under the paragraph: About me, and Featured in
  (`src/pages/featured.html`, cards modelled on pawlean.com/work, plus a
  logo wall once there are several). Don't add more links there.

## Rules that keep it clean

- Don't add navigation: no menus, Back links, buttons or bars.
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

- **Colours: light only.** The page background is the soft warm cream
  #FFFBF3 (taken from careerhannah.com; Leret finds it easy on the eyes),
  with the site's forest greens for text and links. No dark mode, no
  theme switch, no pure black or white.
- **Fonts (chosen by Leret, Oct 2026)**: Ultra for headings (LERET
  wordmark, page and post titles); Outfit for subtitles (labels, dates,
  meta lines, ledes); Lacquer for handwritten touches (only the footer's
  "Contact" label and visitor line); EB Garamond for body text and
  captions. Don't add other fonts.
- **The left column must fit on one screen without scrolling**, on a
  small laptop too. Keep it compact; don't add lines to it. Post titles
  show in full (never cut short) with no dividing lines between them.
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
- [x] 2. **Every page uses the two sides**, with less navigation (done
      by hand, 21 Oct 2026).
- [ ] 3. **New photos onto the wall.** When the Sophie test shoot or
      Manchester Fashion Week photos arrive, add the best few to the top
      of the homepage photo wall, credited, as well as to their posts.
- [ ] 4. **Polish pass.** Check spacing, phone layout, both themes, and
      page speed. Fix small things only.

When every item is ticked, design work is limited to small fixes and
consistency; never start a redesign on your own.
