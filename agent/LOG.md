# Site agent log

Newest first. One short entry per daily run, in plain English.

## 2026-10-24 (scheduled run)

- Health check: build and checks pass, external links fine.
- Manchester Fashion Week note still has no photos, so it stays. Substack still 403; the only YouTube video is already on the site. No new post.
- Design step 5 (polish pass) not started; nothing small needed fixing.

## 2026-10-23 (scheduled run)

- Health check: build and checks pass, external links fine.
- Fact update from Leret applied: the intro on the left now reads "I'm Leret Mutkut, an editorial and campaign model based in Manchester…", and Brother Models is no longer named in the About page text, the page descriptions or the hidden structured data (the "affiliation" entry is gone). I also dropped it from one photo description on the homepage. The bookings email and photo credits are unchanged, as asked. SOURCES.md updated; note moved to `inbox/done/`.
- Manchester Fashion Week note still has no photos, so it stays. Substack still 403; the only YouTube video is already on the site. No new post.
- Design step 5 (polish pass) not started; nothing small needed fixing.

## 2026-10-22 (scheduled run)

- Health check: build and checks pass, external links fine.
- Fact update from Leret applied: the degree now reads "BSc Business Administration and Management" (About page, the AI automation post, SOURCES.md), and the cybersecurity role is "Security Product Manager" without "intern" (About page, SOURCES.md). Note moved to `inbox/done/`.
- Manchester Fashion Week note still has no photos, so it stays. Substack still 403; the only YouTube video is already on the site. No new post.
- Design step 5 (polish pass) not started today; nothing small needed fixing, and the check found no problems.

## 2026-10-21 (scheduled run, evening)

- Health check: build and checks pass, external links fine.
- Inbox: the Manchester Fashion Week note still has no photos, so it stays. Substack still 403; the only YouTube video is already on the site. No new post.
- Design step 4 (masonry photo wall) not started: I couldn't read the photos' pixel sizes (the commands that do it needed an approval nobody could give), and the step needs them for each image's width and height. Left unticked so tomorrow's run can pick it up. Nothing on the site changed.

## 2026-10-21 (scheduled run)

- Health check: no problems at the start; external links fine.
- New post: "Test shoot with Sophie", a photo gallery with Sophie Jouvenaar, Neave and Lethabo Kgope credited and linked as the note asked. Resized the 25 photos into `src/images/modeling/sophie-test-shoot/`; the post uses 13 of them. Note moved to `inbox/done/`; the full-size originals stay in `inbox/` for the safety check to clear.
- Design step 3: put three of the test-shoot photos at the top of the homepage photo wall (credited) and four in "Recent work" on the Modelling Portfolio. Ticked off.
- Manchester Fashion Week note: still no photos, left in place. Substack feed still 403; the only YouTube video is already on the site.

## 2026-10-21 (earlier)

- Health check: no problems, external links fine.
- Inbox: Fashion Week and Sophie test shoot notes still have no photos, so I left them in place.
- No new post: Substack feed still 403; the only YouTube video is already on the site.
- Design step 8: added a "Find me *elsewhere.*" list on the homepage (LinkedIn, Substack, YouTube, GitHub, Instagram, each with a ↗). It replaces the small link row in the contact section, which repeated the same links. Steps 4 and 6 stay blocked (see NEEDS).

## 2026-10-20

- Health check: no problems, external links fine.
- Inbox: Fashion Week and Sophie test shoot notes still have no photos, so I left them in place.
- New post: Leret's YouTube video "i finally did it" (2020) is now on the site with the video embedded. The video gives no clear topic, so I filed it under commercial; it's easy to switch to modelling. Substack feed still returns 403 (third day running).
- Design step 7: the contact section now has three numbered options with pre-filled emails: modelling bookings (to Francesca), speaking and community, everything else. Works in both themes and on phones.
- Skipped step 4 (pinned posts): it needs a change to `build.py`, which I can't edit. Step 6 is skipped until Leret says where and when a homepage photo was taken.

## 2026-10-19

- Health check: only the known Subscribe placeholder form ID (already listed for Leret). External links fine.
- Inbox: the Manchester Fashion Week and Sophie test shoot notes are still waiting for their photos, so I left them in place.
- Substack feed returned 403 again and the YouTube page still shows no channel ID, so no new post. Both have now failed two days running.
- Design step 3: homepage sections now have headings with an italic accent word ("Latest *writing.*", "Get in *touch.*"), in both themes and on phones.

## 2026-10-18 — second run

- Health check: only the known Subscribe placeholder form ID (already listed for Leret). External links fine.
- Inbox: Leret's Brother Models headshots arrived. Resized 17 into `src/images/headshots/`, used two (front and side) on the About page in place of the drawings, with alt text and a "Photos: Brother Models" credit. Note moved to `inbox/done/`. The other 15 are ready for the homepage photo and modelling grid (roadmap 5 and 6).
- Design step 2: added a small top menu (Writing, Modelling, About, Contact) beside the theme toggle; it shrinks for phones.
- Substack and YouTube: no new post today (inbox work took priority).
- Problem: I couldn't delete the full-size originals left in `inbox/photos/` (the shell asked for approval). They are removed from git's index but still on disk; please delete that folder.

## 2026-10-18 — first daily run

- Health check: only issue is the Subscribe box's placeholder form ID (in build.py, already listed for Leret). Nothing else broken.
- Inbox empty. Substack feed returned 403 and the YouTube page showed no channel ID, so no new post; will retry tomorrow.
- Design step 1: replaced the homepage tagline with a short first-person hello, with "commercial" and "modelling" as links. The all-posts page has no tag filter yet, so both links currently open the full list.

## 2026-10-18 — set up

- Site agent installed. It runs every morning and publishes on its own.
