/**
 * script.js — all the site's JavaScript, in three small parts:
 *
 *   1. Theme toggle    — dark/light override, remembered in localStorage
 *   2. Post filtering  — tag filter buttons + the header search box,
 *                        sharing ONE filtering function
 *   3. Reading progress— a thin bar that fills as you scroll a post
 *   4. Lightbox        — click-to-enlarge for photo galleries in posts
 *
 * Each part checks whether the elements it needs exist on the current
 * page and quietly does nothing if not, so the same file is safe to
 * load everywhere.
 */

/* ---------------------------------------------------------------------
   1. THEME
   ---------------------------------------------------------------------
   The CSS defines DARK colors by default and LIGHT colors behind either
   (a) the OS preferring light, or (b) an explicit data-theme attribute
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
    // An explicit saved choice wins. Otherwise default to DARK, and only
    // use light when the OS *explicitly* prefers light — so "no
    // preference" lands on dark, matching the design's dark-first intent.
    const explicit = document.documentElement.getAttribute("data-theme");
    if (explicit) return explicit;
    return window.matchMedia("(prefers-color-scheme: light)").matches
      ? "light"
      : "dark";
  }

  // Inline SVG icons for the toggle, matching the 26x26 icons used
  // elsewhere. Shown is the theme you'd switch TO: a moon while in
  // light mode, a sun while in dark mode.
  const MOON_SVG =
    '<svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
    '<path d="M20 14.5A8.5 8.5 0 0 1 9.5 4a8.5 8.5 0 1 0 10.5 10.5z"/></svg>';
  const SUN_SVG =
    '<svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
    '<circle cx="12" cy="12" r="4"/>' +
    '<path d="M12 2v2.5M12 19.5V22M2 12h2.5M19.5 12H22M4.9 4.9l1.8 1.8M17.3 17.3l1.8 1.8M19.1 4.9l-1.8 1.8M6.7 17.3l-1.8 1.8"/></svg>';

  function updateToggleIcon() {
    themeToggle.innerHTML = currentTheme() === "dark" ? SUN_SVG : MOON_SVG;
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
     1b. ALL POSTS overlay (homepage)
     ---------------------------------------------------------------------
     The overlay is a normal element that lives in the page the whole
     time — opening it is just adding a CSS class, not loading a new
     page. That class flips it from invisible/non-interactive to visible
     (the fade is a CSS opacity transition). This "toggle a class on a
     persistent element" pattern is how most modals/overlays work.
  --------------------------------------------------------------------- */
  const overlay = document.getElementById("allPostsOverlay");
  const openOverlay = document.getElementById("seeAllPosts");
  const closeOverlay = document.getElementById("overlayClose");

  if (overlay && openOverlay) {
    function setOverlay(open) {
      overlay.classList.toggle("is-open", open);
      overlay.setAttribute("aria-hidden", String(!open));
      // Stop the page behind from scrolling while the overlay is up.
      document.body.style.overflow = open ? "hidden" : "";
    }

    openOverlay.addEventListener("click", function (event) {
      event.preventDefault();
      setOverlay(true);
    });
    if (closeOverlay) {
      closeOverlay.addEventListener("click", function () {
        setOverlay(false);
      });
    }
    // Click the dark backdrop (outside the inner panel) to close.
    overlay.addEventListener("click", function (event) {
      if (event.target === overlay) {
        setOverlay(false);
      }
    });
    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && overlay.classList.contains("is-open")) {
        setOverlay(false);
      }
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

  /* ------- search reveal (the magnifying-glass button) -------
     The input sits collapsed at width 0 until .is-open lands on its
     wrapper; the CSS transition does the animating. tabindex switches
     so keyboard users can't Tab into an invisible input. */
  const searchBox = document.getElementById("searchBox");
  const searchToggle = document.getElementById("searchToggle");

  function setSearchOpen(open) {
    searchBox.classList.toggle("is-open", open);
    searchToggle.setAttribute("aria-expanded", String(open));
    searchInput.tabIndex = open ? 0 : -1;
    if (open) {
      searchInput.focus();
    }
  }

  if (searchBox && searchToggle && searchInput) {
    searchToggle.addEventListener("click", function () {
      setSearchOpen(!searchBox.classList.contains("is-open"));
    });

    // Escape while typing closes the box and clears the query, so the
    // list returns to its unfiltered state.
    searchInput.addEventListener("keydown", function (event) {
      if (event.key === "Escape") {
        searchInput.value = "";
        // "input" listeners (the live filter, below) react to this
        // synthetic event exactly as if the user had cleared the field.
        searchInput.dispatchEvent(new Event("input", { bubbles: true }));
        setSearchOpen(false);
      }
    });
  }

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
      // Reveal the search box so the pre-filled query is visible.
      if (searchBox) {
        setSearchOpen(true);
      }
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
     3. READING PROGRESS BAR (post pages only)
     ---------------------------------------------------------------------
     A thin accent bar across the top of the window that fills as you
     scroll, so a reader can see how far through a post they are. Every
     post ends with the generated .subscribe box, so its presence is how
     we know we're on a post — no per-post markup needed.

     Progress = how far the page is scrolled out of its total scrollable
     height. requestAnimationFrame batches the update so we're not doing
     layout work on every single scroll event.
  --------------------------------------------------------------------- */
  if (document.querySelector(".subscribe")) {
    const bar = document.createElement("div");
    bar.className = "read-progress";
    document.body.appendChild(bar);

    let ticking = false;
    function updateProgress() {
      const scrollable =
        document.documentElement.scrollHeight - window.innerHeight;
      const pct = scrollable > 0 ? (window.scrollY / scrollable) * 100 : 0;
      bar.style.width = pct + "%";
      ticking = false;
    }
    window.addEventListener("scroll", function () {
      if (!ticking) {
        window.requestAnimationFrame(updateProgress);
        ticking = true;
      }
    });
    updateProgress();
  }

  /* ---------------------------------------------------------------------
     4. LIGHTBOX (photo galleries inside posts)
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
