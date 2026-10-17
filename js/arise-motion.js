/* ═══════════════════════════════════════════════════════
   ARISE POOLS: GOLDEN HOUR MOTION (pairs with css/arise-v2.css)
   Scroll reveals, kinetic headlines, drifting heroes, nav state,
   gold scroll line, count-up stats, trust marquee, and the
   "Book a Design Call" slide-over survey on every page.
   ═══════════════════════════════════════════════════════ */
(function () {
  'use strict';
  var doc = document.documentElement;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  doc.classList.add('js-motion');

  function track(name, params) { try { gtag('event', name, params || {}); } catch (e) {} }

  // ── Nav: transparent over a dark hero, glass after scroll ──
  var nav = document.querySelector('.nav');
  var hasHero = !!document.querySelector('.hero, .page-hero');
  if (nav && !hasHero) nav.classList.add('is-solid');

  // ── Gold scroll line ──
  var bar = document.createElement('div');
  bar.className = 'gh-progress'; bar.setAttribute('aria-hidden', 'true');
  document.body.appendChild(bar);

  var ticking = false;
  function onScroll() {
    var y = window.scrollY, h = doc.scrollHeight - window.innerHeight;
    if (nav) nav.classList.toggle('is-scrolled', y > 40);
    bar.style.transform = 'scaleX(' + (h > 0 ? Math.min(1, y / h) : 0) + ')';
    ticking = false;
  }
  window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  onScroll();

  // ── Interior hero: move the photo into a drifting layer ──
  document.querySelectorAll('.page-hero').forEach(function (ph) {
    var bg = ph.style.backgroundImage;
    if (!bg || ph.querySelector('.ph-bg')) return;
    var layer = document.createElement('div');
    layer.className = 'ph-bg'; layer.style.backgroundImage = bg;
    ph.style.backgroundImage = 'none';
    ph.insertBefore(layer, ph.firstChild);
  });

  // ── Kinetic headline: words rise in ──
  function kinetic(h) {
    if (!h || reduce) return;
    var i = 0;
    (function wrap(node) {
      Array.prototype.slice.call(node.childNodes).forEach(function (n) {
        if (n.nodeType === 3) {
          var frag = document.createDocumentFragment();
          n.textContent.split(/(\s+)/).forEach(function (part) {
            if (!part) return;
            if (/^\s+$/.test(part)) { frag.appendChild(document.createTextNode(part)); return; }
            var w = document.createElement('span'); w.className = 'w';
            var s = document.createElement('span'); s.textContent = part; s.style.animationDelay = (0.12 + i++ * 0.08) + 's';
            w.appendChild(s); frag.appendChild(w);
          });
          node.replaceChild(frag, n);
        } else if (n.nodeType === 1 && n.tagName !== 'BR') { wrap(n); }
      });
    })(h);
    h.classList.add('gh-kin');
  }
  kinetic(document.querySelector('.hero h1'));
  kinetic(document.querySelector('.page-hero h1'));

  // ── Count-up stats ──
  function countUp(el) {
    var m = el.textContent.trim().match(/^(\d+(?:\.\d+)?)(.*)$/);
    if (!m || reduce) return;
    var end = parseFloat(m[1]), suffix = m[2], dec = (m[1].split('.')[1] || '').length, t0 = null;
    function step(t) {
      if (!t0) t0 = t;
      var p = Math.min(1, (t - t0) / 1600), e = 1 - Math.pow(1 - p, 3);
      el.textContent = (end * e).toFixed(dec) + suffix;
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }

  // ── Trust bar becomes a slow marquee ──
  document.querySelectorAll('.trust-bar').forEach(function (tb) {
    var items = tb.querySelectorAll('.trust-item');
    if (items.length < 3 || reduce) return;
    var track = document.createElement('div'); track.className = 'gh-marquee-track';
    for (var r = 0; r < 2; r++) items.forEach(function (it) {
      var c = it.cloneNode(true); if (r) c.setAttribute('aria-hidden', 'true'); track.appendChild(c);
    });
    tb.innerHTML = ''; tb.appendChild(track); tb.classList.add('gh-marquee');
  });

  // ── Scroll reveals ──
  var revealSel = ['.section-heading', '.service-card', '.process-step', '.testimonial-card', '.portfolio-item', '.post-body > *', '.city-badge', '.cta-section-inner', '.lead-survey', '.footer-grid > div', '.gh-rv-me'];
  var clipSel = ['.service-card-img', '.post-figure img', '.gh-clip-me'];
  var groups = new Map();
  function prep(el, cls) {
    if (el.closest('.hero') || el.closest('.page-hero') || el.closest('.gh-drawer')) return;
    el.classList.add(cls);
    var parent = el.parentElement, n = (groups.get(parent) || 0);
    groups.set(parent, n + 1);
    el.style.setProperty('--d', Math.min(n, 6) * 0.08 + 's');
    io.observe(el);
  }
  var io = 'IntersectionObserver' in window ? new IntersectionObserver(function (es) {
    es.forEach(function (en) {
      if (!en.isIntersecting) return;
      en.target.classList.add('in');
      if (en.target.classList.contains('hero-stat-value')) countUp(en.target);
      io.unobserve(en.target);
    });
  }, { threshold: 0.14, rootMargin: '0px 0px -6% 0px' }) : null;
  if (io && !reduce) {
    revealSel.forEach(function (sel) { document.querySelectorAll(sel).forEach(function (el) { prep(el, 'gh-rv'); }); });
    clipSel.forEach(function (sel) { document.querySelectorAll(sel).forEach(function (el) { prep(el, 'gh-clip'); }); });
    document.querySelectorAll('.gold-rule').forEach(function (el) { io.observe(el); });
    document.querySelectorAll('.hero-stat-value').forEach(function (el) { io.observe(el); });
  } else {
    document.querySelectorAll('.gold-rule').forEach(function (el) { el.classList.add('in'); });
  }

  // ── "Book a Design Call" slide-over with the lead survey ──
  var drawer, scrim, lastFocus;
  function ensureAssets(cb) {
    if (window.AriseSurvey && window.AriseSurvey.mount) return cb();
    if (!document.querySelector('link[href*="lead-survey.css"]')) {
      var l = document.createElement('link'); l.rel = 'stylesheet'; l.href = '/css/lead-survey.css?v=20261016'; document.head.appendChild(l);
    }
    var s = document.querySelector('script[src*="lead-survey.js"]');
    if (s && !window.AriseSurvey) { s.addEventListener('load', cb); return; }
    s = document.createElement('script'); s.src = '/js/lead-survey.js?v=20261016b'; s.onload = cb; document.body.appendChild(s);
  }
  function buildDrawer() {
    scrim = document.createElement('div'); scrim.className = 'gh-drawer-scrim';
    drawer = document.createElement('aside');
    drawer.className = 'gh-drawer'; drawer.setAttribute('role', 'dialog'); drawer.setAttribute('aria-modal', 'true'); drawer.setAttribute('aria-label', 'Book a design call');
    var page = (location.pathname.replace(/^\/|\.html$/g, '') || 'home').replace(/\//g, '-');
    drawer.innerHTML =
      '<div class="gh-drawer-head"><button class="gh-drawer-x" type="button" aria-label="Close">&times;</button>' +
        '<div class="eyebrow" style="justify-content:flex-start;margin:0"><div class="eyebrow-line"></div><span class="eyebrow-text">Free 30-minute design call</span></div>' +
        '<h2>Four questions to <em>your backyard.</em></h2></div>' +
      '<div class="gh-drawer-body"><div class="lead-survey" data-source="site-drawer-' + page + '" data-tags="Website Survey, Drawer"></div></div>' +
      '<div class="gh-drawer-foot">Rather talk now? Call <a href="tel:+16232923073">(623) 292-3073</a></div>';
    drawer.setAttribute('aria-hidden', 'true'); drawer.inert = true;
    document.body.appendChild(scrim); document.body.appendChild(drawer);
    scrim.addEventListener('click', closeDrawer);
    drawer.querySelector('.gh-drawer-x').addEventListener('click', closeDrawer);
    document.addEventListener('keydown', function (e) {
      if (!drawer.classList.contains('open')) return;
      if (e.key === 'Escape') closeDrawer();
      if (e.key === 'Tab') {
        var f = drawer.querySelectorAll('button:not([hidden]), input, textarea, a[href]');
        f = Array.prototype.filter.call(f, function (x) { return x.offsetParent !== null; });
        if (!f.length) return;
        if (e.shiftKey && document.activeElement === f[0]) { e.preventDefault(); f[f.length - 1].focus(); }
        else if (!e.shiftKey && document.activeElement === f[f.length - 1]) { e.preventDefault(); f[0].focus(); }
      }
    });
  }
  function openDrawer(origin) {
    lastFocus = document.activeElement;
    if (!drawer) buildDrawer();
    ensureAssets(function () {
      window.AriseSurvey.mount(drawer.querySelector('.lead-survey'));
      requestAnimationFrame(function () {
        drawer.inert = false; drawer.removeAttribute('aria-hidden');
        scrim.classList.add('open'); drawer.classList.add('open'); document.body.classList.add('gh-lock');
        var first = drawer.querySelector('.ls-tile'); if (first) first.focus({ preventScroll: true });
      });
    });
    track('open_survey_drawer', { origin: origin || 'button', page: location.pathname });
  }
  function closeDrawer() {
    if (!drawer) return;
    scrim.classList.remove('open'); drawer.classList.remove('open'); document.body.classList.remove('gh-lock');
    drawer.setAttribute('aria-hidden', 'true'); drawer.inert = true;
    if (lastFocus) lastFocus.focus();
  }
  window.AriseDrawer = { open: openDrawer, close: closeDrawer };

  // Primary CTAs open the drawer; the Dream Center stays one link away.
  function wire(el, label, origin) {
    if (!el) return;
    if (label) el.textContent = label;
    el.setAttribute('href', '#book');
    el.setAttribute('aria-haspopup', 'dialog');
    el.addEventListener('click', function (e) {
      e.preventDefault();
      var dw = document.getElementById('mobileDrawer');
      if (dw && dw.classList.contains('open') && window.toggleMobileMenu) window.toggleMobileMenu();
      openDrawer(origin);
    });
  }
  document.querySelectorAll('.nav-cta').forEach(function (a) { wire(a, 'Book a Design Call', 'nav'); });
  document.querySelectorAll('.mobile-drawer-cta').forEach(function (a) { wire(a, 'Book a Design Call', 'mobile-menu'); });
  document.querySelectorAll('.sticky-cta-btn.primary').forEach(function (a) { wire(a, 'Book a Call', 'sticky'); });
  document.querySelectorAll('[data-book]').forEach(function (a) { wire(a, null, a.getAttribute('data-book') || 'inline'); });
  document.querySelectorAll('.cta-section .btn-gold[href="/configurator"]').forEach(function (a) {
    wire(a, 'Book a Design Call', 'cta-band');
    if (!a.parentElement.querySelector('.gh-cta-alt')) {
      var alt = document.createElement('span'); alt.className = 'gh-cta-alt';
      alt.innerHTML = 'or price it yourself in the <a href="/configurator">Dream Center</a>';
      a.insertAdjacentElement('afterend', alt);
    }
  });
  if (location.hash === '#book') setTimeout(function () { openDrawer('deep-link'); }, 400);
})();
