/* The ogre's small behaviours: an idle bob (CSS), an occasional blink, a wiggle
   on hover and a spin plus a short message on click. Applies to the header logo
   and the larger hero ogre on the home page.

   Material's document$ emits on first load and again after every instant
   navigation, so setup runs per page. Each ogre is wrapped once and marked, and
   blink timers stop by themselves when their image leaves the page.

   With prefers-reduced-motion set there's no idle animation, blinking, wiggle
   or spin; a click still shows the message. */
(function () {
  "use strict";

  var reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

  var MESSAGES = [
    "Rawr. Back to the logs.",
    "Ogres have layers. So do disk images.",
    "No IOCs here, just a mask.",
    "Hash verified: definitely a mask.",
    "You found me. Chain of custody noted.",
    "I only bite malware."
  ];

  function blinkSrc(img) {
    return new URL("logo-blink.png", img.src).href;
  }

  function scheduleBlink(ogre, openSrc, closedSrc, minMs, maxMs) {
    var wait = minMs + Math.random() * (maxMs - minMs);
    window.setTimeout(function () {
      var img = ogre.img;
      if (!img.isConnected) return;
      if (!reducedMotion.matches && !document.hidden) {
        var blinks = Math.random() < 0.2 ? 2 : 1;
        (function blink(left) {
          img.src = closedSrc;
          window.setTimeout(function () {
            img.src = openSrc;
            if (left > 1) window.setTimeout(function () { blink(left - 1); }, 160);
          }, 130);
        })(blinks);
      }
      scheduleBlink(ogre, openSrc, closedSrc, minMs, maxMs);
    }, wait);
  }

  function play(body, name) {
    if (reducedMotion.matches) return;
    body.classList.remove("sleuth-ogre--wiggle", "sleuth-ogre--spin");
    void body.offsetWidth; /* restart the animation if it's already running */
    body.classList.add("sleuth-ogre--" + name);
  }

  function say(wrap) {
    var old = wrap.querySelector(".sleuth-ogre__say");
    if (old) old.remove();
    var bubble = document.createElement("span");
    bubble.className = "sleuth-ogre__say";
    bubble.setAttribute("role", "status");
    bubble.textContent = MESSAGES[Math.floor(Math.random() * MESSAGES.length)];
    wrap.appendChild(bubble);
    window.setTimeout(function () {
      bubble.classList.add("sleuth-ogre__say--out");
      window.setTimeout(function () { bubble.remove(); }, 300);
    }, 2600);
  }

  function setup(img, kind) {
    if (img.dataset.sleuthOgre) return;
    img.dataset.sleuthOgre = kind;

    /* wrap holds the message bubble; body inside it takes the wiggle and spin,
       so the message stays level while the ogre moves. */
    var wrap = document.createElement("span");
    wrap.className = "sleuth-ogre sleuth-ogre--" + kind;
    var body = document.createElement("span");
    body.className = "sleuth-ogre__body";
    img.parentNode.insertBefore(wrap, img);
    wrap.appendChild(body);
    body.appendChild(img);

    var openSrc = img.src;
    var closedSrc = blinkSrc(img);
    new Image().src = closedSrc; /* preload, so the first blink doesn't flicker */

    wrap.addEventListener("mouseenter", function () {
      if (!body.classList.contains("sleuth-ogre--spin")) play(body, "wiggle");
    });
    body.addEventListener("animationend", function (event) {
      if (event.target === body) body.classList.remove("sleuth-ogre--wiggle", "sleuth-ogre--spin");
    });

    function poke() {
      play(body, "spin");
      say(wrap);
    }

    if (kind === "header") {
      /* The header logo is the home link. On the home page it would only reload
         the page, so it plays instead; everywhere else it navigates as usual. */
      var link = wrap.closest("a");
      link.addEventListener("click", function (event) {
        if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
        if (new URL(link.href).pathname !== window.location.pathname) return;
        event.preventDefault();
        poke();
      });
    } else {
      img.setAttribute("role", "button");
      img.setAttribute("tabindex", "0");
      img.setAttribute("title", "Poke the ogre");
      img.addEventListener("click", poke);
      img.addEventListener("keydown", function (event) {
        if (event.key === "Enter" || event.key === " ") {
          event.preventDefault();
          poke();
        }
      });
    }

    var ogre = { img: img };
    if (kind === "header") scheduleBlink(ogre, openSrc, closedSrc, 6000, 14000);
    else scheduleBlink(ogre, openSrc, closedSrc, 3000, 8000);
  }

  function init() {
    document.querySelectorAll(".md-header__button.md-logo img").forEach(function (img) {
      setup(img, "header");
    });
    document.querySelectorAll(".md-typeset .sleuth-hero__logo").forEach(function (img) {
      setup(img, "hero");
    });
  }

  if (typeof window.document$ !== "undefined") {
    window.document$.subscribe(init);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
