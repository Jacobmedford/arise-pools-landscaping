/* ═══════════════════════════════════════════════════════
   ARISE POOLS — SHARED SITE JS
   Hero slideshow · mobile nav · sticky CTAs · contact → GHL
   ═══════════════════════════════════════════════════════ */
(function () {
  'use strict';

  // ─── Hero slideshow (only on pages that have one) ───
  function initHero() {
    var slides = document.querySelectorAll('.hero-slide');
    var dots = document.querySelectorAll('.hero-dot');
    if (slides.length < 2) return;
    var current = 0;
    function show(n) {
      slides.forEach(function (s) { s.classList.remove('active'); });
      dots.forEach(function (d) { d.classList.remove('active'); });
      slides[n].classList.add('active');
      if (dots[n]) dots[n].classList.add('active');
    }
    dots.forEach(function (dot, i) {
      dot.addEventListener('click', function () { current = i; show(current); });
    });
    setInterval(function () {
      current = (current + 1) % slides.length;
      show(current);
    }, 5500);
  }

  // ─── Mobile menu ───
  window.toggleMobileMenu = function () {
    var hamburger = document.getElementById('hamburger');
    var drawer = document.getElementById('mobileDrawer');
    if (!hamburger || !drawer) return;
    hamburger.classList.toggle('open');
    drawer.classList.toggle('open');
    document.body.style.overflow = drawer.classList.contains('open') ? 'hidden' : '';
  };

  // ─── Accordion sub-menu ───
  window.toggleSub = function (el) {
    el.classList.toggle('open');
    var sub = el.querySelector('.mobile-sub');
    if (sub) sub.classList.toggle('open');
  };

  // ─── GHL webhook ───
  var GHL_WEBHOOK = 'https://services.leadconnectorhq.com/hooks/UJDIrAYT4M5omfYGthyJ/webhook-trigger/a72f86e0-76a1-4489-a3d6-6dccb8f55e94';

  function postToGHL(payload) {
    return fetch(GHL_WEBHOOK, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
  }

  // ─── Contact form handler ───
  function initContactForm() {
    var form = document.getElementById('contactForm');
    if (!form) return;
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var btn = form.querySelector('.btn-submit');
      var status = document.getElementById('contactStatus');
      var data = {
        first_name: (form.firstName.value || '').trim(),
        last_name: (form.lastName.value || '').trim(),
        email: (form.email.value || '').trim(),
        phone: (form.phone.value || '').trim(),
        service_type: form.service.value || '',
        vision_notes: (form.message.value || '').trim(),
        tags: 'Website Contact Form',
        source: 'contact-page',
        submitted_at: new Date().toISOString()
      };

      // Simple validation
      if (!data.first_name || !data.email || !data.phone) {
        if (status) {
          status.textContent = 'Please add your name, email, and phone so we can reach you.';
          status.className = 'form-status error';
        }
        return;
      }

      if (btn) { btn.disabled = true; btn.textContent = 'Sending…'; }
      postToGHL(data)
        .then(function (res) {
          if (status) {
            status.textContent = 'Thank you — your message is on its way. We’ll be in touch within one business day.';
            status.className = 'form-status success';
          }
          form.reset();
        })
        .catch(function () {
          if (status) {
            status.textContent = 'Something went wrong sending your message. Please call us at (480) 555-POOL.';
            status.className = 'form-status error';
          }
        })
        .finally(function () {
          if (btn) { btn.disabled = false; btn.textContent = 'Send Message'; }
        });
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    initHero();
    initContactForm();
  });
})();
