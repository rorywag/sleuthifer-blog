/* GoatCounter page views (cookieless, no banner needed).

   GoatCounter's automatic count on load is turned off (no_onload), and this
   script counts on every emission of Material's document$ instead: once on
   first load and once after each instant navigation, so every page view is
   counted exactly once.

   The path is passed explicitly from location. By default count.js reads the
   <link rel="canonical"> tag, which may still hold the previous page's URL
   after an instant navigation.

   The endpoint is set in the config as well as on the script tag's
   data-goatcounter attribute. count.js looks the tag up on every count, and
   instant navigation swaps the page <head>, which removes the tag; without
   the config fallback, every count after the first would be dropped.

   count.js is self-hosted rather than loaded from gc.zgo.at, so no third-party
   script runs on the site; only the page-view beacon goes to GoatCounter.
   vendor/goatcounter-count-v2.7.0.js is GoatCounter's public/count.js at tag
   v2.7.0 (commit 7e91d8a9bdbb0dd48496e498c5680f8f3477a1b4), unmodified, ISC
   licensed. SHA-256:
   030ad75a7c80a04107a9b91f79e4b1572da0a583a80a9b67e111b310da11cbe9
   To update, download public/count.js from a newer tag, save it under a new
   versioned name, check its hash, and change SCRIPT below. */
(function () {
  "use strict";

  var ENDPOINT = "https://sleuthifer.goatcounter.com/count";
  // Resolved against this file's own URL, so it works from any page depth.
  var SCRIPT = new URL("vendor/goatcounter-count-v2.7.0.js", document.currentScript.src).href;

  window.goatcounter = window.goatcounter || {};
  window.goatcounter.no_onload = true;
  window.goatcounter.endpoint = ENDPOINT;

  /* Page views that happen before count.js has loaded are queued with their
     own path, then sent in order once it loads. */
  var queue = [];

  function send(path) {
    window.goatcounter.count({ path: path });
  }

  function countPageView() {
    var path = window.location.pathname + window.location.search;
    if (typeof window.goatcounter.count === "function") send(path);
    else queue.push(path);
  }

  var script = document.createElement("script");
  script.async = true;
  script.src = SCRIPT;
  script.setAttribute("data-goatcounter", ENDPOINT);
  script.addEventListener("load", function () {
    if (typeof window.goatcounter.count !== "function") return;
    while (queue.length) send(queue.shift());
  });
  document.head.appendChild(script);

  if (typeof window.document$ !== "undefined") {
    window.document$.subscribe(countPageView);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", countPageView);
  } else {
    countPageView();
  }
})();
