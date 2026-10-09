/* ═══════════════════════════════════════════════════════
   ARISE POOLS: PORTFOLIO GALLERIES
   Any element with data-project="<slug>" opens that project's
   photos in an in-page lightbox. Add a project = add an entry here
   and drop its photos in /images/projects/<slug>/.
   ═══════════════════════════════════════════════════════ */
(function () {
  'use strict';

  function P(slug, city) {
    return function (n, w) { return '/images/projects/' + slug + '/' + slug + '-' + city + '-az-' + (n < 10 ? '0' + n : n) + '-' + w + '.jpg'; };
  }

  var PROJECTS = {
    'the-desert-escape': { name: 'The Desert Escape', city: 'Superstition Mountains', img: P('the-desert-escape', 'superstition-mountains'),
      photos: [[7, 'Pool with sheer water features at dusk'], [6, 'Bar seating beside the pool under a mountain sunset'], [5, 'Stacked-stone outdoor kitchen with built-in grill'], [3, 'Covered patio and travertine deck at sunset'], [4, 'Outdoor kitchen wrapped in stacked stone'], [2, 'Aerial view of the pool and travertine patio'], [1, 'Desert front yard landscaping below the Superstitions']] },
    'legacy-living': { name: 'Legacy Living', city: 'San Tan Valley', img: P('legacy-living', 'san-tan-valley'),
      photos: [[3, 'Pool and spa framed by palms at sunset'], [4, 'Raised spa spillover and lawn at sunset'], [6, 'Pool with raised spa spillover'], [2, 'Lounge deck with chaises and pool house'], [8, 'Travertine deck with turf ribbons and spa'], [1, 'Aerial view of the lit pickleball court'], [7, 'Overhead view of the full backyard layout'], [5, 'Front walkway and landscaping at dusk']] },
    'the-hidden-jewel': { name: 'The Hidden Jewel', city: 'Gilbert', img: P('the-hidden-jewel', 'gilbert'),
      photos: [[2, 'Lit step-down pool entry with the covered bar beyond'], [3, 'Freeform pool and spa at twilight'], [1, 'Freeform pool and covered patio at dusk'], [7, 'Covered outdoor bar with TV and seating'], [4, 'Raised spa and fire pit'], [6, 'Refreshed front yard with turf and planters'], [5, 'Front of the home']] },
    'the-modern-escape': { name: 'The Modern Escape', city: 'Gold Canyon', img: P('the-modern-escape', 'gold-canyon'),
      photos: [[1, 'Pool with in-water loungers at dusk'], [4, 'Fire table facing the pool with mountain views'], [2, 'Linear fire table under the covered patio'], [5, 'Pool and patio at blue hour'], [7, 'Aerial view of the pool, spa and turf'], [3, 'Lit desert landscape along the drive'], [6, 'Stone entry courtyard']] },
    'family-focused': { name: 'Family Focused', city: 'Gilbert', img: P('family-focused', 'gilbert'),
      photos: [[1, 'Pool and spa under string lights at night'], [6, 'Pool and lounge chairs at night'], [2, 'Pool with sheer descents and loungers'], [3, 'Turf lawn with pergola bar and yard games'], [4, 'Spa and pool at sunset'], [5, 'Pool and home at night under the moon'], [7, 'Fire pit in the citrus grove']] }
  };

  var tiles = document.querySelectorAll('[data-project]');
  if (!tiles.length) return;

  var lb = document.createElement('div');
  lb.className = 'pg-lb';
  lb.setAttribute('role', 'dialog');
  lb.setAttribute('aria-modal', 'true');
  lb.setAttribute('aria-label', 'Project gallery');
  lb.innerHTML =
    '<div class="pg-top"><div class="pg-title"></div><button class="pg-x" aria-label="Close gallery">&times;</button></div>' +
    '<div class="pg-stage"><button class="pg-nav pg-prev" aria-label="Previous photo">&larr;</button><img alt=""><button class="pg-nav pg-next" aria-label="Next photo">&rarr;</button></div>' +
    '<div class="pg-bottom"><div><span class="pg-count"></span><span class="pg-cap"></span></div>' +
    '<a class="pg-cta" href="/oasis#start">Design One Like This &rarr;</a></div>' +
    '<div class="pg-thumbs"></div>';
  document.body.appendChild(lb);

  var img = lb.querySelector('.pg-stage img'), thumbs = lb.querySelector('.pg-thumbs');
  var cur = { p: null, i: 0 }, lastFocus = null;

  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

  function show() {
    var p = PROJECTS[cur.p], ph = p.photos[cur.i], src = p.img(ph[0], 1800);
    img.style.opacity = 0;
    var pre = new Image();
    pre.onload = pre.onerror = function () { img.src = src; img.alt = ph[1] + ', ' + p.name + ' in ' + p.city + ', AZ'; img.style.opacity = 1; };
    pre.src = src;
    lb.querySelector('.pg-count').textContent = (cur.i + 1) + ' / ' + p.photos.length;
    lb.querySelector('.pg-cap').textContent = ph[1];
    thumbs.querySelectorAll('button').forEach(function (b, k) { b.classList.toggle('on', k === cur.i); });
    var nx = p.photos[(cur.i + 1) % p.photos.length]; (new Image()).src = p.img(nx[0], 1800);
  }

  function open(slug, at) {
    var p = PROJECTS[slug]; if (!p) return;
    lastFocus = document.activeElement;
    cur = { p: slug, i: at || 0 };
    lb.querySelector('.pg-title').innerHTML = esc(p.name) + '<small>' + esc(p.city) + '</small>';
    thumbs.innerHTML = p.photos.map(function (ph, k) {
      return '<button type="button" data-i="' + k + '" aria-label="Photo ' + (k + 1) + '"><img src="' + p.img(ph[0], 900) + '" alt="" loading="lazy"></button>';
    }).join('');
    show();
    lb.classList.add('open');
    document.body.style.overflow = 'hidden';
    lb.querySelector('.pg-x').focus();
    try { gtag('event', 'view_project_gallery', { project: p.name, page: 'portfolio' }); } catch (e) {}
  }

  function close() { lb.classList.remove('open'); document.body.style.overflow = ''; if (lastFocus) lastFocus.focus(); }
  function step(d) { var n = PROJECTS[cur.p].photos.length; cur.i = (cur.i + d + n) % n; show(); }

  lb.querySelector('.pg-prev').onclick = function () { step(-1); };
  lb.querySelector('.pg-next').onclick = function () { step(1); };
  lb.querySelector('.pg-x').onclick = close;
  thumbs.addEventListener('click', function (e) { var b = e.target.closest('[data-i]'); if (b) { cur.i = +b.getAttribute('data-i'); show(); } });
  lb.addEventListener('click', function (e) { if (e.target === lb || e.target.classList.contains('pg-stage')) close(); });
  document.addEventListener('keydown', function (e) {
    if (!lb.classList.contains('open')) return;
    if (e.key === 'Escape') close();
    if (e.key === 'ArrowRight') step(1);
    if (e.key === 'ArrowLeft') step(-1);
    if (e.key === 'Tab') {
      var f = lb.querySelectorAll('button, a'), first = f[0], last = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    }
  });
  var tx = null, stage = lb.querySelector('.pg-stage');
  stage.addEventListener('touchstart', function (e) { tx = e.touches[0].clientX; }, { passive: true });
  stage.addEventListener('touchend', function (e) {
    if (tx === null) return; var dx = e.changedTouches[0].clientX - tx; if (Math.abs(dx) > 40) step(dx < 0 ? 1 : -1); tx = null;
  });

  tiles.forEach(function (t) {
    var slug = t.getAttribute('data-project'), p = PROJECTS[slug];
    if (!p) return;
    t.setAttribute('role', 'button');
    t.setAttribute('tabindex', '0');
    t.setAttribute('aria-label', 'View ' + p.photos.length + ' photos of ' + p.name);
    var badge = document.createElement('span');
    badge.className = 'pg-badge';
    badge.textContent = p.photos.length + ' photos';
    t.appendChild(badge);
    t.addEventListener('click', function () { open(slug, 0); });
    t.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(slug, 0); } });
  });
})();
