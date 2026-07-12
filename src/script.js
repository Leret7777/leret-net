/**
 * script.js — the one piece of real interactivity on the site: the photo
 * gallery lightbox on the Modeling page. Every other page loads this file
 * too (it's in the shared <!-- FOOTER --> markup) but simply has no
 * .gallery__item elements, so nothing below ever runs for them.
 *
 * What a "lightbox" is: clicking a small thumbnail image opens a large
 * version of it in an overlay on top of the page, instead of navigating
 * to a new page. That overlay — the <div class="lightbox"> in
 * modeling.html — is the same single element reused for every photo;
 * we just change which image it's showing and toggle its visibility.
 */

// document.addEventListener runs our code once the page's HTML has
// finished loading, so we're guaranteed the elements we're about to
// query for actually exist in the DOM yet.
document.addEventListener("DOMContentLoaded", function () {
  const lightbox = document.getElementById("lightbox");

  // If this page has no lightbox markup (i.e. we're not on the Modeling
  // page), there's nothing for this script to do.
  if (!lightbox) {
    return;
  }

  const lightboxImage = document.getElementById("lightboxImage");
  const lightboxCaption = document.getElementById("lightboxCaption");
  const closeButton = lightbox.querySelector(".lightbox__close");

  // querySelectorAll returns every element matching the selector, as a
  // static list (a NodeList) we can loop over with forEach.
  const galleryItems = document.querySelectorAll(".gallery__item");

  function openLightbox(imageSrc, captionText) {
    lightboxImage.src = imageSrc;
    lightboxImage.alt = captionText || "";
    lightboxCaption.textContent = captionText || "";

    // Elements with the `hidden` HTML attribute are not rendered at all.
    // removeAttribute("hidden") is how we make it visible again — this
    // is the JS half of the CSS rule `.lightbox[hidden] { display: none; }`.
    lightbox.removeAttribute("hidden");
  }

  function closeLightbox() {
    lightbox.setAttribute("hidden", "");
    // Clear the src so the browser isn't holding a full-size image in
    // memory (and so it doesn't briefly flash the old photo the next
    // time the lightbox opens, before the new src loads).
    lightboxImage.src = "";
  }

  galleryItems.forEach(function (item) {
    item.addEventListener("click", function () {
      // Each gallery button wraps a single <img>. We reuse that image's
      // own src as the lightbox's src — for real photos you'd typically
      // point this at a larger version via a data-full attribute
      // instead; see the comment in modeling.html.
      const img = item.querySelector("img");
      const fullSrc = img.dataset.full || img.src;
      openLightbox(fullSrc, img.alt);
    });
  });

  closeButton.addEventListener("click", closeLightbox);

  // Clicking the dark overlay itself (not the image) should also close
  // it. event.target is whatever element was actually clicked; we only
  // close if that's the lightbox container itself.
  lightbox.addEventListener("click", function (event) {
    if (event.target === lightbox) {
      closeLightbox();
    }
  });

  // Let keyboard users close the lightbox with Escape.
  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape" && !lightbox.hasAttribute("hidden")) {
      closeLightbox();
    }
  });
});
