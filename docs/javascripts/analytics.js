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
   the config fallback, every count after the first would be dropped. */
(function () {
  "use strict";

  var ENDPOINT = "https://sleuthifer.goatcounter.com/count";
  var SCRIPT = "//gc.zgo.at/count.js";

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
