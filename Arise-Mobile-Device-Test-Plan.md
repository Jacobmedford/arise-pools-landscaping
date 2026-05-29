# Arise Pools — Mobile Device Test Plan

**Purpose:** Verify the rebuilt site renders and functions correctly on real devices before any go-live. Run this on the Vercel **preview/staging URL** first. Do not point the production domain at the site until every Blocker-level item passes.

**Test devices (the four agreed targets):**

| Device | Viewport | Notes |
|---|---|---|
| iPhone SE (2nd/3rd gen) | 375 × 667 | Smallest common screen — tightest layout test |
| iPhone 15 Pro | 393 × 852 | Notch / Dynamic Island safe-area |
| Google Pixel 7 | 412 × 915 | Android Chrome rendering |
| iPad (10.9") | 768 × 1024 | Tablet breakpoint — nav switches to desktop here |

Test each device in **both portrait and landscape**, on the device's default browser (Safari for iPhone/iPad, Chrome for Pixel).

---

## How to test

1. Open the Vercel preview URL on the device (or use Safari/Chrome DevTools device mode as a first pass).
2. Walk each page in the checklist below.
3. Mark each row Pass / Fail. Note the device + browser for any failure.
4. Severity: **Blocker** = must fix before go-live · **Minor** = fix soon, not launch-blocking.

---

## 1. Global / every page

- [ ] **Header** — Logo (ARISE & CO.) visible; tapping it returns to home.
- [ ] **Hamburger menu** opens and closes; tapping the icon toggles it; body doesn't scroll behind the open drawer.
- [ ] **Mobile drawer links** all work: Services (expands sub-menu), Portfolio, Process, About, Financing, Reviews, Contact, Begin Your Design.
- [ ] **Services sub-menu accordion** expands/collapses and each of the 6 service links opens the right page.
- [ ] **Sticky bottom CTA bar** ("Design My Backyard" / "Call Now") stays pinned, doesn't cover content, and both buttons work. *(Blocker if it overlaps a form's submit button.)*
- [ ] **"Call Now"** opens the phone dialer with the correct number.
- [ ] **Footer** — all link columns tappable; tap targets not too close together.
- [ ] **No horizontal scroll / no content bleeding off the right edge** on any page. *(Blocker)*
- [ ] **Fonts load** (Cormorant Garamond headings, Jost body) — no fallback flash that sticks.
- [ ] **Images load** and are not stretched/squashed; hero photos fill correctly.
- [ ] **Safe areas (iPhone 15 Pro)** — header and sticky bar not hidden behind the Dynamic Island or home indicator.

## 2. Home (`/`)

- [ ] **Hero headline** "Designed Outdoors. Built Once. Enjoyed Forever" renders on clean lines — **no word breaking mid-word** (this was the defect on the old Wix build). *(Blocker)*
- [ ] Hero slideshow auto-advances; dots are tappable.
- [ ] Stats (200+ / 15+ / 5.0) readable and aligned.
- [ ] Trust bar, Dream Center teaser, portfolio grid, services grid, 7-step method, testimonials, city list, financing strip, closing CTA all stack in single column and read cleanly.
- [ ] All hero + section CTAs route correctly (Design Mine → /configurator, View Portfolio → /portfolio).

## 3. Dream Center (`/configurator`) — **conversion-critical**

- [ ] All **7 steps** advance and go back; progress dots reflect the current step.
- [ ] Service-type **emoji icons** (🏊 🌿 🔄 ✨ etc.) display (they render on real devices even though they may show as boxes in some emulators).
- [ ] Selecting cards highlights them; multi-select features work.
- [ ] Text inputs (name, email, phone, address, vision notes) are tappable, the right keyboard appears (email/number/tel), and the screen doesn't jump.
- [ ] Validation messages appear for missing required fields.
- [ ] On submit: estimate displays, success panel ("Your Vision Is On Its Way") appears.
- [ ] **Lead actually arrives in GoHighLevel** with all fields + tags (test with a real submission — see section 6). *(Blocker)*

## 4. Contact (`/contact`)

- [ ] Form fields stack in a **single column** (not two cramped columns). *(Blocker if side-by-side)*
- [ ] Required-field validation works (name, email, phone).
- [ ] Submit shows the success message and resets the form.
- [ ] **Lead arrives in GoHighLevel** tagged "Website Contact Form." *(Blocker)*
- [ ] Phone and email links work; "Open the Dream Center" button routes to /configurator.

## 5. Other pages

- [ ] **Services overview** (`/services`) — 6 cards tappable, each opens its detail page.
- [ ] **Service detail** (e.g. `/services/custom-pools`) — hero, intro, "Signature Details," related services all render.
- [ ] **City pages** — spot-check at least 3 of the 11 (e.g. `/cities/scottsdale`, `/cities/gilbert`, `/cities/queen-creek`): correct city name throughout, CTA routes to /configurator.
- [ ] **About** (`/about`) — values grid + trust bar stack cleanly.
- [ ] **Process** (`/process`) — 7 steps render in order.
- [ ] **Financing** (`/financing`) — "Home Improvement Loans" named; example payment strip readable.
- [ ] **Portfolio** (`/portfolio`) — image grid loads, overlays legible on tap.

## 6. GoHighLevel lead-flow test (do this live)

1. Submit the **Dream Center** with test data (use a recognizable name like "TEST Mobile iPhoneSE").
2. Submit the **Contact form** with another test entry.
3. In GoHighLevel, confirm both contacts arrived with: name, email, phone, and the expected tags (`Dream Center Lead` / `Website Contact Form`; "Hot Lead — Next 3 Months" if timeline = next 3 months).
4. Confirm any GHL automation/notification you expect actually fires.
5. Delete the test contacts when done.

## 7. Performance (quick pass)

- [ ] Home loads in a reasonable time on cellular (hero images are large — watch for slow first paint).
- [ ] Scrolling is smooth, no jank on the slideshow.
- [ ] *(Optional)* Run Lighthouse mobile in Chrome DevTools; note Performance and Accessibility scores.

---

## Sign-off

| Device | Portrait pass | Landscape pass | Blockers found | Tester / date |
|---|---|---|---|---|
| iPhone SE | ☐ | ☐ | | |
| iPhone 15 Pro | ☐ | ☐ | | |
| Pixel 7 | ☐ | ☐ | | |
| iPad | ☐ | ☐ | | |

**Go-live gate:** All Blocker items pass on all four devices **and** the GoHighLevel lead-flow test confirms leads arriving. Only then point the production domain at the site.
