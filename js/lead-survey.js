/* ═══════════════════════════════════════════════════════
   ARISE POOLS: LEAD SURVEY (one question at a time)
   Drop <div class="lead-survey" data-source="homepage-survey" data-tags="Website Survey"></div>
   anywhere, load /css/lead-survey.css and this file. Leads post straight to the
   GHL inbound webhook (workflow "New website - Engagement") plus the n8n sheet backup,
   then go to /book. Budget and timeline values match the GHL custom fields
   Budget Range and Timeline exactly.
   ═══════════════════════════════════════════════════════ */
(function () {
  'use strict';

  var GHL_WEBHOOK = 'https://services.leadconnectorhq.com/hooks/UJDIrAYT4M5omfYGthyJ/webhook-trigger/eea6dd51-7c5a-4039-a711-9dcf2a965dd6';
  var SHEET_BACKUP = 'https://jacobmed.app.n8n.cloud/webhook/ariseoasis';

  var SERVICES = [
    { v: 'Pool', img: '/images/projects/legacy-living/legacy-living-san-tan-valley-az-06-900.jpg' },
    { v: 'Landscape', img: '/images/projects/legacy-living/legacy-living-san-tan-valley-az-08-900.jpg' },
    { v: 'Remodel', img: '/images/projects/the-hidden-jewel/the-hidden-jewel-gilbert-az-02-900.jpg' },
    { v: 'Outdoor Living', img: '/images/projects/the-desert-escape/the-desert-escape-superstition-mountains-az-05-900.jpg' },
    { v: 'Fire & Water Features', img: '/images/projects/the-modern-escape/the-modern-escape-gold-canyon-az-02-900.jpg' },
    { v: 'Hardscape & Sport Courts', img: '/images/projects/legacy-living/legacy-living-san-tan-valley-az-01-900.jpg' }
  ];
  // value = GHL "Budget Range" option ('' when it has no matching option)
  var BUDGETS = [
    { v: '', label: 'Under $50k' },
    { v: '50-100k', label: '$50k to $100k' },
    { v: '100-200k', label: '$100k to $200k' },
    { v: '200-350k', label: '$200k to $350k' },
    { v: '350k+', label: '$350k and up' },
    { v: '', label: 'Not sure yet' }
  ];
  // value = GHL "Timeline" option
  var TIMELINES = [
    { v: 'next-3-months', label: 'Within 3 months' },
    { v: '3-6-months', label: '3 to 6 months' },
    { v: '6-12-months', label: '6 to 12 months' },
    { v: 'exploring', label: 'Just exploring' }
  ];
  var ATTR_KEYS = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term', 'gclid', 'fbclid'];

  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function track(name, params) { try { gtag('event', name, params || {}); } catch (e) {} }

  var attribution = (function () {
    var qs = new URLSearchParams(location.search), out = {}, saved = {};
    try { saved = JSON.parse(sessionStorage.getItem('arise_attr') || '{}'); } catch (e) {}
    ATTR_KEYS.forEach(function (k) { out[k] = qs.get(k) || saved[k] || ''; });
    try { sessionStorage.setItem('arise_attr', JSON.stringify(out)); } catch (e) {}
    return out;
  })();

  var instances = [];

  function build(root, idx) {
    var source = root.getAttribute('data-source') || 'website-survey';
    var tagBase = root.getAttribute('data-tags') || 'Website Survey';
    var heading = root.getAttribute('data-heading') || '';
    var uid = 'ls' + idx;
    var st = { step: 1, services: [], budget: null, timeline: null, inspired: [] };

    function opts(list, name) {
      return list.map(function (o, k) {
        return '<button type="button" class="ls-opt" data-' + name + '="' + k + '" aria-pressed="false">' + esc(o.label) + '</button>';
      }).join('');
    }

    root.innerHTML =
      '<form class="ls-card" novalidate>' +
        (heading ? '<div class="ls-head">' + esc(heading) + '</div>' : '') +
        '<div class="ls-progress" aria-hidden="true"><i></i><i></i><i></i><i></i></div>' +
        '<div class="ls-step" data-step="1">' +
          '<div class="ls-label">Question 1 of 4</div>' +
          '<h3 class="ls-q">What are we building?</h3>' +
          '<p class="ls-hint">Pick everything that applies.</p>' +
          '<div class="ls-tiles">' + SERVICES.map(function (s) {
            return '<button type="button" class="ls-tile" data-svc="' + esc(s.v) + '" aria-pressed="false"><img src="' + s.img + '" alt="" loading="lazy"><span>' + esc(s.v) + '</span></button>';
          }).join('') + '</div>' +
          '<p class="ls-err" role="alert"></p>' +
          '<div class="ls-actions"><span></span><button type="button" class="ls-btn" data-next>Next &rarr;</button></div>' +
        '</div>' +
        '<div class="ls-step" data-step="2" hidden>' +
          '<div class="ls-label">Question 2 of 4</div>' +
          '<h3 class="ls-q">What budget do you have in mind?</h3>' +
          '<p class="ls-hint">A rough range is fine. It helps us bring the right ideas to your call.</p>' +
          '<div class="ls-opts">' + opts(BUDGETS, 'budget') + '</div>' +
          '<div class="ls-actions"><button type="button" class="ls-back" data-back>&larr; Back</button><span></span></div>' +
        '</div>' +
        '<div class="ls-step" data-step="3" hidden>' +
          '<div class="ls-label">Question 3 of 4</div>' +
          '<h3 class="ls-q">When would you like to start?</h3>' +
          '<div class="ls-opts">' + opts(TIMELINES, 'timeline') + '</div>' +
          '<div class="ls-actions"><button type="button" class="ls-back" data-back>&larr; Back</button><span></span></div>' +
        '</div>' +
        '<div class="ls-step" data-step="4" hidden>' +
          '<div class="ls-label">Last step</div>' +
          '<h3 class="ls-q">Where should we send your call details?</h3>' +
          '<p class="ls-summary"></p>' +
          '<div class="ls-fields">' +
            '<label class="ls-field"><span>First name</span><input name="first_name" autocomplete="given-name" required></label>' +
            '<label class="ls-field"><span>Last name</span><input name="last_name" autocomplete="family-name" required></label>' +
            '<label class="ls-field"><span>Phone</span><input name="phone" type="tel" inputmode="tel" autocomplete="tel" required></label>' +
            '<label class="ls-field"><span>Email</span><input name="email" type="email" autocomplete="email" required></label>' +
            '<label class="ls-field ls-full"><span>Anything else we should know? (optional)</span><textarea name="vision_notes" placeholder="Lot size, what is there now, must-haves..."></textarea></label>' +
            '<div class="ls-hp" aria-hidden="true"><label>Company<input name="company" tabindex="-1" autocomplete="off"></label></div>' +
          '</div>' +
          '<p class="ls-err" role="alert" id="' + uid + '-err"></p>' +
          '<div class="ls-actions"><button type="button" class="ls-back" data-back>&larr; Back</button><button type="submit" class="ls-btn ls-submit">Book My Design Call &rarr;</button></div>' +
          '<p class="ls-fine">By submitting, you agree Arise Pools &amp; Landscaping may call, text or email you about your project. Message and data rates may apply. Reply STOP to opt out. See our <a href="/privacy">privacy policy</a>.</p>' +
        '</div>' +
      '</form>';

    var form = root.querySelector('form');
    var bars = root.querySelectorAll('.ls-progress i');

    function show(n) {
      st.step = n;
      root.querySelectorAll('.ls-step').forEach(function (s) { s.hidden = +s.getAttribute('data-step') !== n; });
      bars.forEach(function (b, k) { b.classList.toggle('on', k < n); });
      var first = root.querySelector('.ls-step[data-step="' + n + '"] input, .ls-step[data-step="' + n + '"] .ls-tile, .ls-step[data-step="' + n + '"] .ls-opt');
      if (first) first.focus({ preventScroll: true });
      if (n === 4) renderSummary();
      if (n > 1) track('survey_step', { step: n, source: source });
    }
    function renderSummary() {
      var bits = [st.services.join(', ')];
      if (st.budget !== null) bits.push(BUDGETS[st.budget].label);
      if (st.timeline !== null) bits.push('start ' + TIMELINES[st.timeline].label.toLowerCase());
      if (st.inspired.length) bits.push('inspired by ' + st.inspired.join(', '));
      root.querySelector('.ls-summary').textContent = '✓ ' + bits.join(' · ');
    }
    function syncTiles() {
      root.querySelectorAll('[data-svc]').forEach(function (el) { el.setAttribute('aria-pressed', st.services.indexOf(el.getAttribute('data-svc')) > -1); });
    }

    root.addEventListener('click', function (e) {
      var t = e.target.closest('[data-svc]');
      if (t) {
        var v = t.getAttribute('data-svc'), k = st.services.indexOf(v);
        if (k > -1) st.services.splice(k, 1); else st.services.push(v);
        syncTiles(); root.querySelector('.ls-step[data-step="1"] .ls-err').textContent = ''; return;
      }
      var b = e.target.closest('[data-budget]');
      if (b) { st.budget = +b.getAttribute('data-budget'); pick(b, '[data-budget]'); setTimeout(function () { show(3); }, 220); return; }
      var tl = e.target.closest('[data-timeline]');
      if (tl) { st.timeline = +tl.getAttribute('data-timeline'); pick(tl, '[data-timeline]'); setTimeout(function () { show(4); }, 220); return; }
      if (e.target.closest('[data-next]')) {
        if (!st.services.length) { root.querySelector('.ls-step[data-step="1"] .ls-err').textContent = 'Pick at least one so we know where to start.'; return; }
        show(2); return;
      }
      if (e.target.closest('[data-back]')) show(Math.max(1, st.step - 1));
    });
    function pick(el, sel) { root.querySelectorAll(sel).forEach(function (o) { o.setAttribute('aria-pressed', o === el); }); }

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var err = root.querySelector('#' + uid + '-err'); err.textContent = '';
      var f = { first: form.first_name, last: form.last_name, phone: form.phone, email: form.email };
      var names = { first: 'first name', last: 'last name', phone: 'a 10-digit phone number', email: 'a valid email' };
      var bad = [];
      if (!f.first.value.trim()) bad.push('first');
      if (!f.last.value.trim()) bad.push('last');
      if (f.phone.value.replace(/\D/g, '').length < 10) bad.push('phone');
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(f.email.value.trim())) bad.push('email');
      Object.keys(f).forEach(function (k) { var x = bad.indexOf(k) > -1; f[k].classList.toggle('bad', x); f[k].setAttribute('aria-invalid', x); f[k].setAttribute('aria-describedby', uid + '-err'); });
      if (bad.length) { err.textContent = 'Please add your ' + bad.map(function (k) { return names[k]; }).join(', ') + '.'; f[bad[0]].focus(); return; }
      if (!st.services.length) { show(1); return; }
      if (st.budget === null) { show(2); return; }
      if (st.timeline === null) { show(3); return; }

      var notes = form.vision_notes.value.trim();
      if (st.inspired.length) notes = 'Inspired by: ' + st.inspired.join(', ') + (notes ? '\n' + notes : '');
      var budget = BUDGETS[st.budget], timeline = TIMELINES[st.timeline];
      var utm = ['utm_source', 'utm_medium', 'utm_campaign'].map(function (k) { return attribution[k] ? k + '=' + attribution[k] : ''; }).filter(Boolean).join(' ');
      // Sheet backup columns only (Google Sheet auto-maps by header name).
      var payload = {
        first_name: f.first.value.trim(),
        last_name: f.last.value.trim(),
        email: f.email.value.trim(),
        phone: f.phone.value.trim(),
        service_type: st.services.join(', '),
        budget_range: budget.v,
        timeline: timeline.v,
        vision_notes: notes,
        tags: tagBase + (utm ? ', ' + utm : ''),
        source: source,
        submitted_at: new Date().toISOString()
      };
      var ghlPayload = Object.assign({}, payload, attribution, {
        budget_label: budget.label,
        timeline_label: timeline.label,
        project_description: ['Services: ' + payload.service_type, 'Budget: ' + budget.label, 'Start: ' + timeline.label, notes ? 'Notes: ' + notes : ''].filter(Boolean).join('\n'),
        landing_page: location.origin + location.pathname
      });

      var btn = root.querySelector('.ls-submit');
      btn.disabled = true; btn.textContent = 'Sending...';
      function done() {
        try { sessionStorage.setItem('arise_first_name', payload.first_name); } catch (x) {}
        window.location.href = '/book';
      }
      if (form.company.value) { done(); return; }
      track('generate_lead', { form: source, services: payload.service_type, budget: budget.label, timeline: timeline.label });
      var post = function (url, body) { return fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body), keepalive: true }).then(function (r) { if (!r.ok) throw new Error(r.status); return true; }); };
      var toGhl = post(GHL_WEBHOOK, ghlPayload).catch(function () { return post(GHL_WEBHOOK, ghlPayload); }).then(function () { return true; }, function () { return false; });
      var toSheet = post(SHEET_BACKUP, payload).then(function () { return true; }, function () { return false; });
      // Captured if it reached GHL or the sheet backup.
      Promise.all([toGhl, toSheet]).then(function (r) { if (!r[0] && !r[1]) throw new Error('both failed'); }).then(done, function () {
        btn.disabled = false; btn.innerHTML = 'Book My Design Call &rarr;';
        err.innerHTML = 'Something went wrong sending that. Please try again or call us at <a href="tel:+16232923073">(623) 292-3073</a>.';
      });
    });

    return {
      root: root,
      addService: function (v) { if (st.services.indexOf(v) < 0) { st.services.push(v); syncTiles(); } },
      setInspiration: function (name, on) {
        var k = st.inspired.indexOf(name);
        if (on && k < 0) st.inspired.push(name);
        if (!on && k > -1) st.inspired.splice(k, 1);
        if (st.step === 4) renderSummary();
      }
    };
  }

  document.querySelectorAll('.lead-survey').forEach(function (el, i) { instances.push(build(el, i)); });

  // Small API for pages that want to pre-fill the survey (the /oasis "save as inspiration" buttons).
  window.AriseSurvey = {
    addService: function (v) { instances.forEach(function (s) { s.addService(v); }); },
    setInspiration: function (name, on) { instances.forEach(function (s) { s.setInspiration(name, on); }); }
  };
})();
