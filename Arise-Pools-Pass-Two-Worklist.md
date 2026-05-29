# Arise Pools — Pass Two Work List

Companion to the Master Blueprint. Everything below is ready to execute the moment the Wix staging URL lands.

> **LAUNCH POSTURE: STAGING ONLY.** Do not publish to the live domain. Do not point DNS. Set staging to `noindex` until client gives explicit "go live" approval. The goal is that launch day = one publish click + DNS swap, with zero scramble.

---

## 1. CMS Collections — exact schemas

Create these in Wix Studio → CMS. Permissions: "Anyone" read where noted, "Admin" write everywhere else.

### Portfolio
| Field | Type | Notes |
|---|---|---|
| title | Text | Required |
| slug | Text | URL, auto from title |
| city | Reference → Cities | |
| style | Tags | Modern, Resort, Infinity, Lagoon, Plunge, Mediterranean, Desert Contemporary |
| featured | Boolean | Show on home grid |
| hero | Image | 2400×1600, WebP |
| gallery | Gallery | 8–14 images |
| story | Rich text | 250–400 words |
| specs | Object | size, depth, features[], hardscape[], duration_weeks, budget_band |
| completed_at | Date | |
| seo_title | Text | |
| seo_description | Text | |

Read: Anyone.

### Cities
| Field | Type | Notes |
|---|---|---|
| name | Text | "Gilbert, AZ" |
| slug | Text | |
| hero_image | Image | |
| intro | Rich text | 150 words, local voice |
| climate_note | Text | e.g. "East Valley — intense summer sun, monsoon drainage considerations" |
| hoa_notes | Rich text | Common HOA requirements in this city |
| local_projects | Reference-multi → Portfolio | |
| local_testimonials | Reference-multi → Testimonials | |
| zip_codes | Tags | For "do you serve my area" logic |
| population | Number | |
| seo_title | Text | |
| seo_description | Text | |

### Services
| Field | Type | Notes |
|---|---|---|
| title | Text | |
| slug | Text | |
| pillar | Tag | Pool / Landscape / Hardscape / Structure / Feature / Maintenance |
| hero | Image | |
| short_description | Text | 30 words, nav/teaser use |
| body | Rich text | |
| faqs | Reference-multi → FAQs | |
| related_portfolio | Reference-multi → Portfolio | |
| starting_price_note | Text | "Projects typically start at $85,000" |

### Testimonials
name · city · rating (1–5) · quote · project (ref Portfolio) · source (Google/Yelp/Houzz) · verified (bool) · published (bool)

### BlogPosts
title · slug · author (ref TeamMembers) · published_at · hero · excerpt · body (rich) · category (tag) · related_services · seo_title · seo_description

### DreamSubmissions (lead capture — private, admin only)
submitted_at · vision · style · features[] · hardscape · structures[] · lot_size · timeline · budget_band · estimate_low · estimate_high · name · email · phone · address · zip · inspiration_files · booking_id · ghl_synced (bool) · ghl_contact_id · status (New/Contacted/Booked/Lost/Won)

### TeamMembers
name · slug · title · bio · headshot · years_experience · specialties[] · featured

### Awards
title · issuer · year · image · link

### FAQs
question · answer (rich) · category (tag) · display_order

---

## 2. Velo Code — Dream Center configurator

Drop into a Velo page file on `/dream-center`. Requires CMS collection `DreamSubmissions` and Wix Bookings service configured for "Consultation - 60 min".

### `/dream-center` page code

```javascript
// pages/dream-center.js
import wixData from 'wix-data';
import wixLocation from 'wix-location';
import { fetch } from 'wix-fetch';
import { session } from 'wix-storage';

const STATE_KEY = 'dream_center_state';

const STEPS = [
  { id: 'vision',     title: 'Your vision',    type: 'single' },
  { id: 'style',      title: 'Your style',     type: 'single' },
  { id: 'features',   title: 'Features',       type: 'multi'  },
  { id: 'hardscape',  title: 'Hardscape',      type: 'single' },
  { id: 'structures', title: 'Structures',     type: 'multi'  },
  { id: 'lot',        title: 'Size & lot',     type: 'single' },
  { id: 'timeline',   title: 'Timeline & budget', type: 'compound' }
];

// Estimate engine — tuned from Master Blueprint pricing
const BASE = { newPool: 95000, remodel: 45000, landscapeOnly: 25000, fullBackyard: 180000 };
const FEATURE_ADD = {
  spa: 18000, waterfall: 6500, fireBowl: 3200, bajaShelf: 5500,
  swimUpBar: 9500, deckJets: 4200, ledLighting: 2800, autoCover: 14000
};
const HARDSCAPE_MULT = { travertine: 1.15, flagstone: 1.22, pavers: 1.08, stamped: 1.0, none: 0 };
const STRUCTURE_ADD = { ramada: 22000, pergola: 14000, outdoorKitchen: 28000, firePitLounge: 8500 };
const LOT_MULT = { small: 0.92, medium: 1.0, large: 1.15, estate: 1.35 };

export function calculateEstimate(state) {
  const base = BASE[state.vision] || 0;
  const features = (state.features || []).reduce((sum, f) => sum + (FEATURE_ADD[f] || 0), 0);
  const structures = (state.structures || []).reduce((sum, s) => sum + (STRUCTURE_ADD[s] || 0), 0);
  const hardscape = state.hardscape && state.hardscape !== 'none'
    ? base * (HARDSCAPE_MULT[state.hardscape] - 1) : 0;
  const subtotal = base + features + structures + hardscape;
  const adjusted = subtotal * (LOT_MULT[state.lot] || 1);
  // Present as range ±12% for honesty
  return {
    low: Math.round(adjusted * 0.88 / 1000) * 1000,
    high: Math.round(adjusted * 1.12 / 1000) * 1000
  };
}

$w.onReady(() => {
  const state = JSON.parse(session.getItem(STATE_KEY) || '{}');
  renderStep(state.currentStep || 0, state);
});

function renderStep(idx, state) {
  // wire up #stepRepeater, #nextBtn, #backBtn, #progressBar
  // on next: save to state, persist to session, advance idx
  // on final: calculate estimate, show summary, reveal contact form + Bookings widget
}

export async function onSubmit(formData) {
  const state = JSON.parse(session.getItem(STATE_KEY) || '{}');
  const estimate = calculateEstimate(state);

  const record = {
    ...state,
    ...formData,
    estimate_low: estimate.low,
    estimate_high: estimate.high,
    submitted_at: new Date(),
    status: 'New',
    hubspot_synced: false
  };

  const saved = await wixData.insert('DreamSubmissions', record);

  // Fire GoHighLevel webhook (backend function)
  await syncToGHL(saved);

  session.removeItem(STATE_KEY);
  wixLocation.to(`/consultation?ref=${saved._id}`);
}
```

### Backend: `backend/ghl.jsw` (GoHighLevel integration)

```javascript
import { fetch } from 'wix-fetch';
import { getSecret } from 'wix-secrets-backend';

// GHL Inbound Webhook (set up via Workflows → Triggers → Inbound Webhook)
export async function syncToGHL(submission) {
  const webhookUrl = await getSecret('GHL_DREAM_WEBHOOK');
  const firstName = submission.name?.split(' ')[0] || '';
  const lastName = submission.name?.split(' ').slice(1).join(' ') || '';

  // GHL custom fields — must match the field keys created in the GHL sub-account
  const payload = {
    firstName,
    lastName,
    email: submission.email,
    phone: submission.phone,
    address1: submission.address,
    postalCode: submission.zip,
    source: 'Website - Dream Center',
    tags: ['dream-center', `vision-${submission.vision}`, `budget-${submission.budget_band}`],
    customField: {
      dream_vision: submission.vision,
      dream_style: submission.style,
      dream_features: (submission.features || []).join(', '),
      dream_hardscape: submission.hardscape,
      dream_structures: (submission.structures || []).join(', '),
      dream_lot_size: submission.lot_size,
      dream_timeline: submission.timeline,
      dream_budget_band: submission.budget_band,
      dream_estimate_low: submission.estimate_low,
      dream_estimate_high: submission.estimate_high,
      dream_submission_id: submission._id
    }
  };

  const res = await fetch(webhookUrl, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });

  if (res.ok) {
    const body = await res.json().catch(() => ({}));
    return { synced: true, ghl_contact_id: body.contact_id || null };
  }
  return { synced: false };
}
```

**GoHighLevel setup checklist:**
- Create dedicated sub-account for Arise Pools (or use existing)
- Create custom fields matching keys above: `dream_vision`, `dream_style`, `dream_features`, `dream_hardscape`, `dream_structures`, `dream_lot_size`, `dream_timeline`, `dream_budget_band`, `dream_estimate_low`, `dream_estimate_high`, `dream_submission_id`
- Create tags: `dream-center`, `vision-newPool`, `vision-remodel`, `vision-landscapeOnly`, `vision-fullBackyard`, `budget-75-125k`, `budget-125-200k`, `budget-200-350k`, `budget-350k+`
- Build "Inbound Webhook" trigger in Workflows → copy webhook URL
- Store URL in Wix Secrets Manager as `GHL_DREAM_WEBHOOK`
- Build lead-response automation in GHL:
  - Instant SMS + email to contact (warm, editorial tone)
  - Internal notification to sales rep
  - 7-day nurture sequence if no consultation booked in 48 hrs
  - Pipeline stage: New Lead → Consultation Booked → Site Visit Complete → Proposal Sent → Won/Lost

---

## 3. City page template

One dynamic page at `/cities/{slug}` bound to the Cities collection. Section order:

1. Editorial hero — city-specific photo + headline "Custom pools in {city}, Arizona."
2. Intro paragraph — 150 words, local voice (Cities.intro).
3. Local projects — dataset filter `city = current` on Portfolio, 6 projects.
4. Climate & HOA note — Cities.climate_note + Cities.hoa_notes side-by-side.
5. Local testimonials — 3 from Testimonials filtered by city.
6. Neighboring cities — cards linking to 3 nearest Cities entries.
7. City-specific CTA — "Book a {city} consultation" → Dream Center with `?city={slug}` prefilled.
8. Local LocalBusiness + Place JSON-LD injected via Wix SEO.

Each city page auto-generates unique meta title, description, OG image from the collection.

---

## 4. Redirect map — old arisepal.com → new structure

Set up in Wix SEO → URL Redirects. 301s.

| From | To |
|---|---|
| `/custom-pools` | `/services/custom-pools` |
| `/landscaping` | `/services/landscaping` |
| `/remodels` | `/services/pool-remodels` |
| `/maintenance` | `/services/pool-service` |
| `/outdoor-living` | `/services/outdoor-living-rooms` |
| `/portfolio` | `/signature-work` |
| `/portfolio/:slug` | `/signature-work/:slug` |
| `/blog` | `/journal` |
| `/blog/:slug` | `/journal/:slug` |
| `/fountain-hills-pools` | `/cities/fountain-hills` |
| `/cave-creek-pools` | `/cities/cave-creek` |
| `/contact` | `/contact` (keep) |
| `/financing` | `/financing` (keep) |
| `/about` | `/about` (keep) |
| `/get-quote` | `/dream-center` |
| `/free-estimate` | `/dream-center` |
| `/quote` | `/dream-center` |

---

## 5. Apps to install on staging site

1. Wix Bookings — service: "On-site consultation (60 min)". Buffer 30 min. Only Mon–Sat. Confirmation email uses Arise template.
2. Wix Forms — only for ancillary contact form (Dream Center is custom Velo).
3. Wix Blog — for /journal.
4. Wix SEO — full schema injection.
5. GA4 — via Wix Analytics + custom events: `dream_step_complete`, `dream_submit`, `book_consult_click`, `phone_click`.
6. Google Tag Manager — embed in head, managed server-side.
7. Meta Pixel — Lead + CompleteRegistration events on Dream submit.
8. Microsoft Clarity — session replay for conversion debugging.
9. HubSpot — via webhook (above), no native app needed.

---

## 6. Launch checklist

- [ ] All 47 pages created, nav + footer wired
- [ ] Brand tokens applied (cream bg, Cormorant + Jost, gold-dark for text-on-cream)
- [ ] Dream Center 7-step Velo flow live, estimate engine verified against 3 known projects
- [ ] Wix Bookings connected to Dream summary
- [ ] HubSpot webhook firing (test submission with real email)
- [ ] Confirmation email: elegant, Cormorant header, no emojis
- [ ] All 11 city pages populated from Cities CMS
- [ ] 12+ portfolio projects loaded with gallery + story
- [ ] 15+ Google reviews pulled into Testimonials collection
- [ ] Schema.org validated (Rich Results Test) on Home, Service, City, Project, FAQ
- [ ] Lighthouse: Performance ≥ 90, A11y ≥ 95, SEO = 100
- [ ] WCAG 2.1 AA: contrast audit, keyboard nav, focus rings, skip-link, alt text
- [ ] Redirects all return 301
- [ ] XML sitemap submitted to Search Console
- [ ] `robots.txt` clean, staging noindex until DNS cutover
- [ ] GA4, Clarity, Meta Pixel firing on staging
- [ ] Mobile tested on iPhone SE + Pixel 7 + iPad

---

## 7. Mobile build standard (first-class, not an afterthought)

Wix Studio has separate breakpoint controls per section. Every page must be tuned at each of these widths — not left to auto-scale. "Done" requires manual review at all four.

**Test matrix**
| Device | Width | Priority |
|---|---|---|
| iPhone SE (2022) | 375px | P0 — smallest common |
| iPhone 15 Pro | 393px | P0 |
| Pixel 7 | 412px | P0 |
| iPad Mini (portrait) | 768px | P1 |
| iPad Pro (landscape) | 1024px | P1 |

**Mobile rules — enforce on every page**
- Tap targets ≥ 44×44px. No exceptions. Especially: Dream Center tiles, nav dropdown items, footer links.
- Thumb zone — primary CTA (Dream Center / Book Consult) reachable one-handed. Sticky bottom bar on mobile with "Call" + "Book Consult" + "Dream Center" (3 equal buttons, stone bg, gold active state).
- Hamburger menu — full-screen overlay, Cormorant section labels, generous 24px vertical spacing between links. Phone number + "Book Consult" button pinned at bottom of the overlay.
- Hero on mobile — reduce headline from 64px → 36px. Two CTAs stack vertically, full-width.
- Images — all `<img>` use `loading="lazy"` except hero. Serve WebP. Max 180KB each on mobile.
- Section padding — desktop 120px → mobile 56px. Never less than 40px.
- Typography — body text 16px minimum on mobile (never 14px). Line height 1.6+.
- Dream Center on mobile — steps render as full-screen cards with one question at a time. Progress bar fixed to top. Next/Back buttons fixed to bottom. Avoid any horizontal scroll.
- Portfolio grid — 1 column mobile, 2 columns tablet, 3 columns desktop. Captions below image, not overlaid on mobile.
- City grid — 1 column mobile with 24px gap, not cramped.
- Forms — every input full-width, labels stacked above (not placeholder-only), 48px input height, `inputmode` attributes set (tel, email, numeric).
- Review carousel — swipe-enabled on mobile, pagination dots, no auto-advance on mobile (battery + reduced-motion).
- Footer — stack to 1 column on mobile, collapse service/city lists into accordions.
- No horizontal scroll anywhere. Audit every page by scrolling left-right; nothing should move.
- Safe area insets — respect iPhone notch and bottom home bar on sticky elements.

**Mobile launch gate — all must be green**
- [ ] Every page tested manually on iPhone SE, iPhone 15, Pixel 7, iPad
- [ ] Lighthouse Mobile: Performance ≥ 85, A11y ≥ 95, Best Practices ≥ 95, SEO = 100
- [ ] LCP ≤ 2.5s on 4G throttled, CLS ≤ 0.1, INP ≤ 200ms
- [ ] Sticky mobile CTA bar present and functional
- [ ] Dream Center fully usable thumb-only, no pinch-zoom required
- [ ] Tap target audit — no violations in Chrome DevTools
- [ ] Forms submit successfully on iOS Safari + Android Chrome
- [ ] Click-to-call on phone numbers (`tel:` links)
- [ ] Bookings widget renders cleanly on mobile (Wix's default is janky — may need custom wrapper)
- [ ] No content reflow / layout shift on font load (preload Cormorant + Jost)
- [ ] Tested in both portrait and landscape on phones

---

## 8. Pre-launch master gate (must be 100% before publish)

Launch day should be boring: flip `noindex` off → publish → point DNS → submit sitemap. Everything below must be done, tested, and signed off on staging FIRST.

**Content**
- [ ] All 47 pages built and populated (no Lorem Ipsum, no placeholder images)
- [ ] All 11 city pages localized with real projects, testimonials, HOA notes
- [ ] 12+ portfolio projects with full galleries + written stories
- [ ] 15+ Google reviews mirrored into Testimonials CMS
- [ ] 8 pillar blog posts published
- [ ] About / Founder page with real photo + bio + video (or placeholder noted for phase 2)

**Design**
- [ ] Brand tokens applied site-wide (no stray default Wix colors/fonts)
- [ ] Cormorant Garamond + Jost loaded via Google Fonts, `font-display: swap`, preloaded
- [ ] Gold-dark (#8B6914) used for any gold text on cream — never #C9A464
- [ ] Hairline dividers only — no shadows, no gradients, no rounded-full pills

**Functionality**
- [ ] Dream Center 7-step flow completes end-to-end on desktop + mobile
- [ ] Estimate engine sanity-checked against 3 real recent projects (should be within ±15%)
- [ ] DreamSubmissions CMS receives test submission with all fields populated
- [ ] HubSpot webhook returns 200 and contact appears in HubSpot
- [ ] Wix Bookings: consultation service configured, hours/buffer set, test booking works + confirmation email received
- [ ] Confirmation email elegant, Cormorant header, Arise branding, no emojis
- [ ] All forms have honeypot + reCAPTCHA enabled
- [ ] 404 page branded and helpful (not default Wix)

**Accessibility (WCAG 2.1 AA)**
- [ ] Axe DevTools: 0 critical, 0 serious issues site-wide
- [ ] Contrast: all text ≥ 4.5:1, large text ≥ 3:1
- [ ] Keyboard: full site navigable without mouse, visible focus rings everywhere
- [ ] Skip-to-content link on every page
- [ ] All images have meaningful alt text (decorative images empty alt="")
- [ ] `prefers-reduced-motion` disables carousels and auto-advance
- [ ] Form error messages programmatically associated with inputs (aria-describedby)
- [ ] Nav dropdowns keyboard-operable (Enter/Space/Arrow keys)

**Performance**
- [ ] Lighthouse Desktop: Performance ≥ 90
- [ ] Lighthouse Mobile: Performance ≥ 85
- [ ] Hero image ≤ 300KB WebP, preloaded
- [ ] All images WebP with responsive `srcset`
- [ ] Video (founder) lazy-loaded, poster frame, no autoplay with sound
- [ ] Third-party scripts deferred or via GTM
- [ ] No render-blocking resources

**SEO**
- [ ] Unique meta title + description on every page (no duplicates)
- [ ] LocalBusiness schema on every page (via Wix SEO or custom `<script>`)
- [ ] Service schema on 8 pillar pages
- [ ] Place schema on 11 city pages
- [ ] Article schema on blog posts
- [ ] FAQPage schema where FAQs appear
- [ ] Review / AggregateRating schema on Reviews page
- [ ] OpenGraph + Twitter card images on every page
- [ ] XML sitemap generated and valid
- [ ] `robots.txt` set to allow (staging stays `noindex` via Wix SEO setting, flipped on launch)
- [ ] All redirects from section 4 configured and return 301
- [ ] Rich Results Test passes on Home, Service, City, Project, FAQ, Blog

**Analytics & tracking**
- [ ] GA4 firing pageviews + custom events (`dream_step_complete`, `dream_submit`, `book_consult_click`, `phone_click`)
- [ ] Google Tag Manager installed, container published
- [ ] Meta Pixel firing Lead + CompleteRegistration on Dream submit
- [ ] Microsoft Clarity session replay live
- [ ] Google Business Profile linked, reviews pulling
- [ ] Test conversion goal fires end-to-end (Dream submit → GA4 + Meta + HubSpot)

**Legal & trust**
- [ ] Privacy Policy (AZ + CCPA compliant)
- [ ] Terms of Service
- [ ] Accessibility Statement
- [ ] Cookie banner (GDPR-ready even though mostly AZ traffic)
- [ ] ROC license numbers visible in footer
- [ ] BBB badge linked (if applicable)

**Infrastructure & ops**
- [ ] Custom domain reserved in Wix but NOT yet pointed
- [ ] DNS change plan documented (current host, TTL lowered to 300s 24hrs before cutover)
- [ ] Current arisepal.com content archived (HTML snapshot saved)
- [ ] 301 redirect map from old URLs tested on staging via URL rewrite
- [ ] Admin user accounts + permissions set for client team
- [ ] Client trained on: editing CMS, adding portfolio projects, reviewing Dream submissions, responding via HubSpot

**Stakeholder signoff**
- [ ] Client walkthrough on desktop + mobile
- [ ] Client written approval to publish
- [ ] Cutover window scheduled (avoid Monday mornings / weekend — prefer Tuesday-Thursday 9–11am MT when support is fresh)

---

## 10. Client-confirmed decisions (2026-04-15)

**Resolved:**
- ✅ "15+ years" copy — **approved, keep as-is** site-wide.
- ✅ Founder video — **hold for phase 2.** Use portrait + pull-quote only on Founder Moment section; leave video slot in the CMS for later.
- ✅ CRM integration — **GoHighLevel (NOT HubSpot).** Client will provide sub-account access. Use GHL Inbound Webhook on a Workflow trigger, not HubSpot API. Worklist updated.
- ✅ Financing partner — **Home Improvement Loans.** Display their logo + "From $299/mo with approved credit · Home Improvement Loans" on Financing page + home strip. (Need confirmed rate/term copy + logo asset from client.)
- ✅ Photography — **client will upload real project photos.** We stage placeholders in Portfolio CMS with WebP slots ready; client drops originals into shared folder, we compress + caption.
- ✅ Blog — **ghostwrite 8 pillar posts.** Draft outlines + finished pieces on our side; client reviews before publishing. Topics to cover: pool styles for AZ climate, remodel vs new build, choosing hardscape in the desert, pool maintenance myths, financing a backyard, HOA navigation in East Valley, picking a builder (due diligence checklist), timeline expectations.
- ✅ Service area — **11 cities total.** Added **Fountain Hills** and **Cave Creek** to the original 9 (Gilbert, Chandler, Mesa, Queen Creek, Scottsdale, Paradise Valley, Tempe, Ahwatukee, San Tan Valley). City page count: 11. Total sitemap: 49 pages.
- ✅ Google Business Profile — client provided: https://share.google/fvvHzfd56Jv5bBpqw. Pull live review count, star rating, and top reviews before launch for Reviews page + Testimonials CMS seed. (Do not clickthrough here — verify URL destination before any fetch.)

**Still open (low-risk, can be resolved during build):**
- ROC license number re-verification (currently using #342276 & #342277 from prototype).
- GoHighLevel sub-account credentials + webhook URL (client to provide when GHL workspace is set up).
- Home Improvement Loans — logo file + approved rate/term marketing copy.
- Sales team user accounts for Wix admin + GHL pipeline.
