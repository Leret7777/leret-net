(Not a post: a fact update from Leret, 22 Oct 2026.)

Leret doesn't want the agency advertised on the site. Say the kind of
model Leret is: "editorial and campaign model, based in Manchester".

Change these:

1. Homepage intro, the left column on every page (src/partials/nav.html,
   the paragraph under LERET). Make it:
   "I'm Leret Mutkut, an editorial and campaign model based in
   Manchester. By day I build AI automation for commercial and sales
   teams."
   Keep it this short: the left column must still fit on one screen.

2. About page (src/pages/about.html):
   - Opening paragraph: replace "I'm also a model with Brother Models,
     and I live in Manchester." with "I'm also an editorial and campaign
     model, and I live in Manchester."
   - "Modelling" section: remove "I'm represented by Brother Models."
     Keep the bookings sentence and email: "For bookings, email my agent
     Francesca at francesca@brothermodels.com".

3. The hidden descriptions on the homepage and About page (the
   <meta name="description"> lines and the structured-data block at the
   top, the one with "@type": "Person"): remove "represented by Brother
   Models" from the descriptions, and remove the whole "affiliation"
   entry that names Brother Models. Keep "name": "Leret Mutkut" and
   everything else.

Keep exactly as they are:
- The bookings email (francesca@brothermodels.com) in the contact
  footer and on the Modelling Portfolio.
- Photo credits ("Polaroids: Brother Models", "Photos: Brother Models"):
  they credit who took the photos.
- Image file names.
- The Modelling Portfolio page.

Also add to "Facts about me" in agent/SOURCES.md: "Describe Leret as an
editorial and campaign model based in Manchester. Don't name the agency
in intros, the About page or page descriptions; the bookings email and
photo credits stay." Don't change anything else.
