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
- **Alignment on the left:** the intro (LERET, paragraph, page links)
  and the contact footer are centred; the Writing list is left-aligned.
  The three sections are evenly spaced, footer close under the list.
- **Two quiet page links** under the paragraph: About me, and Featured in
  (`src/pages/featured.html`, cards modelled on pawlean.com/work, plus a
  logo wall once there are several). Don't add more links there.

## Rules that keep it clean

- Don't add navigation: no menus, Back links, buttons or bars.
- Add photos, not sections. New photos Leret approves go on the photo
  wall and/or in the relevant post. Order the wall by type, never by
  date or shoot, in this order (Leret's instruction):
  1. **Close-ups**: tight shots where Leret's face or a detail fills the
     frame.
  2. **Face**: headshots and portraits, head and shoulders.
  3. **Half body**: Leret alone, waist or hips up.
  4. **With others**: any shot with another person in it.
  5. **Full body**: Leret alone, head to toe.
  The first three photos stay as Leret chose them: the eye-and-ring
  close-up (sophie-test-shoot-11), the front-on polaroid close-up
  (headshots/8) and the black and white shot leaning on the brick wall
  (sophie-test-shoot-02). Within each group, mix shoots,
  colour and black and white. Put each new photo into the right group.
  Current photos, sorted by Leret's groups:
  - Close-ups: sophie-test-shoot-11, headshots/8, sophie-test-shoot-02,
    headshots/9, sophie-test-shoot-09, headshots/1
  - Face: headshots/10, headshots/3, headshots/12, headshots/11
  - Half body: headshots/2, headshots/13, headshots/5, headshots/14,
    headshots/4, headshots/15, headshots/6, headshots/16, headshots/7
  - With others: sophie-test-shoot-04, -13, -06, -12, -01, -08, -07, -05
  - Full body: sophie-test-shoot-10, headshots/17, sophie-test-shoot-03
- **Photos are never cropped**, on the wall or anywhere else: always the
  whole photo, at its own shape. The wall is an irregular masonry layout,
  not a grid of identical rows (see roadmap item 4).
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
- **Free fonts only.** Every font on the site must be free to use on a
  website, including for work (in practice: Google Fonts). Never use a
  font that is only "free for personal use" or needs a paid licence.
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
- [x] 3. **New photos onto the wall.** When the Sophie test shoot or
      Manchester Fashion Week photos arrive, add the best few to the top
      of the homepage photo wall, credited, as well as to their posts.
      (Sophie test shoot done 21 Oct 2026; add the Fashion Week photos the
      same way if they arrive.)
- [x] 4. **Irregular photo wall, no cropping, like sophiejouvenaar.com
      (done by hand 21 Oct 2026: masonry in script.js; when adding a photo,
      put its <button> in the right group in src/pages/index.html; the
      width/height attributes are optional)
      (Leret asked for this on 21 Oct 2026; do it next).** Sophie's wall
      (checked 21 Oct 2026) is a masonry layout: 3 equal-width columns,
      about 10px gaps, and every photo shown whole at its own shape
      (portrait, landscape or square), so the columns end at different
      heights. Photos are placed left, middle, right, then each next one
      goes under whichever column is shortest, so the order reads across
      the top. Do the same on the homepage wall:
      - **Never crop a photo.** In `src/style.css`, remove the fixed
        `aspect-ratio` from `.photo-wall .gallery__item`, and make the
        images `width: 100%; height: auto;` with no `object-fit: cover`.
      - **Masonry, not identical rows**: 3 columns on wide screens, 2 on
        phones and narrow screens, gaps about 10px (6px on phones),
        square corners.
      - **Keep the order** in the "Order the wall by type" rule above,
        reading across the top. Don't use plain CSS `columns` (it fills
        column 1 first). In `src/script.js`, place the photos into the
        columns one by one, each into whichever column is currently
        shortest, using each photo's width and height so it works before
        images finish loading (add `width` and `height` attributes to each
        `<img>` in `src/pages/index.html`, taken from the image files).
        Rebuild when the screen changes between 2 and 3 columns. Without
        JavaScript the photos must still show whole, in order, one under
        another.
      - Reorder the photos in `src/pages/index.html` to match the groups
        listed in that rule.
      - Keep click-to-enlarge working, and the photo credit line under the
        wall.
      - Check: no photo is cut off, the top starts with headshots/8 then
        sophie-test-shoot-02, and nothing scrolls sideways on a phone.
- [ ] 5. **Polish pass.** Check spacing, phone layout and page speed.
      Fix small things only.

When every item is ticked, design work is limited to small fixes and
consistency; never start a redesign on your own.
