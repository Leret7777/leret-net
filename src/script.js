/**
 * script.js — all the site's JavaScript, in three small parts:
 *
 *   1. Theme toggle  — dark/light override, remembered in localStorage
 *   2. Post filtering — tag filter buttons + the header search box,
 *                       sharing ONE filtering function
 *   3. Lightbox      — click-to-enlarge for photo galleries in posts
 *
 * Each part checks whether the elements it needs exist on the current
 * page and quietly does nothing if not, so the same file is safe to
 * load everywhere.
 */

/* ---------------------------------------------------------------------
   1. THEME
   ---------------------------------------------------------------------
   The CSS defines light colors by default and dark colors behind either
   (a) the OS-level preference or (b) an explicit data-theme attribute
   on <html>. All this code does is manage that attribute.

   This first bit runs immediately (not waiting for DOMContentLoaded):
   the sooner the attribute is set, the less chance of a flash of the
   wrong theme while the page loads.
--------------------------------------------------------------------- */
(function () {
  const saved = localStorage.getItem("theme"); // "dark", "light", or null
  if (saved === "dark" || saved === "light") {
    document.documentElement.setAttribute("data-theme", saved);
  }
})();

document.addEventListener("DOMContentLoaded", function () {
  /* ------- theme toggle button ------- */
  const themeToggle = document.getElementById("themeToggle");

  function currentTheme() {
    // Explicit choice wins; otherwise fall back to the OS preference.
    // matchMedia lets JS evaluate the same query the CSS uses.
    const explicit = document.documentElement.getAttribute("data-theme");
    if (explicit) return explicit;
    return window.matchMedia("(prefers-color-scheme: dark)").matches
      ? "dark"
      : "light";
  }

  function updateToggleIcon() {
    // Show the theme you'd switch TO: a moon while in light mode,
    // a sun while in dark mode.
    themeToggle.textContent = currentTheme() === "dark" ? "☀" : "☾";
  }

  if (themeToggle) {
    updateToggleIcon();
    themeToggle.addEventListener("click", function () {
      const next = currentTheme() === "dark" ? "light" : "dark";
      document.documentElement.setAttribute("data-theme", next);
      localStorage.setItem("theme", next); // survives page loads
      updateToggleIcon();
    });
  }

  /* ---------------------------------------------------------------------
     2. POST FILTERING (tags + search together)
     ---------------------------------------------------------------------
     Two inputs, one output: the visible set of posts.

       - activeTag: which tag pill is selected ("all" = no tag filter)
       - query:     whatever's typed in the search box

     A post stays visible only if it passes BOTH tests. Keeping a single
     applyFilters() function — instead of separate "search code" and
     "tag code" — means the two can never disagree about what should be
     shown, and adding a third filter someday (e.g. by year) would just
     be one more condition in the same place.
  --------------------------------------------------------------------- */
  const postList = document.getElementById("postList");
  const searchInput = document.getElementById("siteSearch");
  const tagFilterRow = document.getElementById("tagFilters");

  if (postList) {
    const items = Array.from(postList.querySelectorAll(".post-list__item"));
    const tagButtons = tagFilterRow
      ? Array.from(tagFilterRow.querySelectorAll(".tag-filter"))
      : [];

    // A "no results" message we create once and show when needed.
    const noResults = document.createElement("p");
    noResults.className = "no-results";
    noResults.textContent = "No posts match — try a different tag or search.";
    noResults.hidden = true;
    postList.after(noResults);

    let activeTag = "all";
    let query = "";

    function applyFilters() {
      let visibleCount = 0;

      items.forEach(function (item) {
        // data-tags="modeling,work" -> ["modeling", "work"]
        const tags = item.dataset.tags ? item.dataset.tags.split(",") : [];
        const tagOk = activeTag === "all" || tags.includes(activeTag);

        // Match the query against everything readable in the entry
        // (title, date, tags, excerpt) — textContent collects it all.
        const text = item.textContent.toLowerCase();
        const textOk = query === "" || text.includes(query);

        const show = tagOk && textOk;
        item.hidden = !show; // [hidden] posts are display:none via CSS
        if (show) visibleCount++;
      });

      noResults.hidden = visibleCount !== 0;

      // Keep the pill highlighting in sync with activeTag.
      tagButtons.forEach(function (btn) {
        btn.classList.toggle("is-active", btn.dataset.tag === activeTag);
      });
    }

    tagButtons.forEach(function (btn) {
      btn.addEventListener("click", function () {
        activeTag = btn.dataset.tag;
        applyFilters();
      });
    });

    if (searchInput) {
      // The "input" event fires on every keystroke (and on clearing the
      // field), so the list filters live as you type.
      searchInput.addEventListener("input", function () {
        query = searchInput.value.trim().toLowerCase();
        applyFilters();
      });
    }

    // Support arriving with ?q=...&tag=... in the URL (e.g. from the
    // search box on another page). URLSearchParams parses the query
    // string for us.
    const params = new URLSearchParams(window.location.search);
    const urlQuery = params.get("q");
    const urlTag = params.get("tag");
    if (urlQuery && searchInput) {
      searchInput.value = urlQuery;
      query = urlQuery.trim().toLowerCase();
    }
    if (urlTag && tagButtons.some((b) => b.dataset.tag === urlTag)) {
      activeTag = urlTag;
    }
    applyFilters();
  } else if (searchInput) {
    // Not on the homepage: there's no list here to filter, so pressing
    // Enter sends the query to the homepage instead.
    searchInput.addEventListener("keydown", function (event) {
      if (event.key === "Enter" && searchInput.value.trim() !== "") {
        window.location.href =
          "/?q=" + encodeURIComponent(searchInput.value.trim());
      }
    });
  }

  /* ---------------------------------------------------------------------
     3. LIGHTBOX (photo galleries inside posts)
     ---------------------------------------------------------------------
     Clicking a gallery thumbnail opens the image large in an overlay —
     the single hidden <div class="lightbox"> at the bottom of any post
     that has a gallery. We just swap its <img> src and toggle the
     `hidden` attribute.
  --------------------------------------------------------------------- */
  const lightbox = document.getElementById("lightbox");
  if (lightbox) {
    const lightboxImage = document.getElementById("lightboxImage");
    const lightboxCaption = document.getElementById("lightboxCaption");
    const closeButton = lightbox.querySelector(".lightbox__close");
    const galleryItems = document.querySelectorAll(".gallery__item");

    function openLightbox(imageSrc, captionText) {
      lightboxImage.src = imageSrc;
      lightboxImage.alt = captionText || "";
      lightboxCaption.textContent = captionText || "";
      lightbox.removeAttribute("hidden");
    }

    function closeLightbox() {
      lightbox.setAttribute("hidden", "");
      // Clear the src so the browser isn't holding a full-size image in
      // memory, and so the old photo doesn't flash next time it opens.
      lightboxImage.src = "";
    }

    galleryItems.forEach(function (item) {
      item.addEventListener("click", function () {
        const img = item.querySelector("img");
        // data-full can point at a larger version than the thumbnail;
        // fall back to the thumbnail itself if it's not set.
        openLightbox(img.dataset.full || img.src, img.alt);
      });
    });

    closeButton.addEventListener("click", closeLightbox);

    // Clicking the dark backdrop (not the image) also closes it.
    lightbox.addEventListener("click", function (event) {
      if (event.target === lightbox) {
        closeLightbox();
      }
    });

    // And so does the Escape key.
    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && !lightbox.hasAttribute("hidden")) {
        closeLightbox();
      }
    });
  }
});
