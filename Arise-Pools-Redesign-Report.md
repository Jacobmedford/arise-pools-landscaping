# Arise Pools & Landscaping — Website Audit & Wix Rebuild Blueprint

**Prepared for:** Arise Pools & Landscaping (Gilbert, AZ)
**Prepared by:** Design team
**Date:** April 15, 2026
**Scope:** Full audit of the new React prototype (`arise-pools-website.zip`) + cross-reference to live `arisepal.com` + Wix recreation plan with luxury elevation and an interactive Dream Center.

---

## 1. Executive Summary

The uploaded prototype is a well-architected React + Vite + Tailwind + shadcn/ui codebase (~2,300 lines across 28 page/component files) with a clear luxury direction — Cormorant Garamond display serif, Jost body sans, gold/cream/stone/pool-blue palette, and a dedicated Dream Center section. Navigation, IA, SEO metadata, and schema.org markup are already strong.

What's missing for a **"luxury dream center" experience** that converts:

1. The Dream Center is currently a **static card grid** that links to marketing pages — not an interactive configurator. This is the single biggest gap between the prototype and the client's stated goal.
2. **Accessibility hits several WCAG 2.1 AA violations** (color contrast on gold-on-cream, text-on-image gradients, missing focus styles, icon-only links, motion without reduced-motion guard).
3. **Performance risk** — three unoptimized hero JPEGs auto-rotate, Google Fonts are loaded via blocking `@import`, and Framer Motion animates nearly every section.
4. **Luxury cues are inconsistent** — the palette is correct but spacing, typography rhythm, and photography treatment need tightening for a true premium feel.
5. **Wix rebuild** requires deliberate mapping: Wix Studio + Velox (Velo) code for the configurator, CMS collections for portfolio/blog, and a Wix Forms/HubSpot-integrated lead flow.

**Overall score of uploaded prototype: 74 / 100** — great foundation, not yet luxury-tier. This document provides the exact component-by-component path to get there in Wix.

---

## 2. What Was Audited

| Asset | Source | Notes |
|---|---|---|
| React prototype | `arise-pools-website.zip` (uploaded) | 13 pages, 14 custom components, 50+ shadcn UI primitives, Framer Motion animations |
| Live site | `arisepal.com` | Wix Thunderbolt render; confirms client is currently on Wix (Editor, not Studio). Live copy and imagery pulled where accessible. |
| Brand tokens | `src/index.css`, `tailwind.config.ts` | HSL CSS variables; Cormorant Garamond + Jost |
| SEO/Schema | `index.html` | LocalBusiness JSON-LD already present (good) |
| Content | All page `.tsx` files | Copy voice, CTAs, service taxonomy |

---

## 3. Information Architecture — Current State

```
/                           Home (Hero slider → Dream Center → Services → Testimonials → CTA)
/custom-pools               Signature Pools
/landscaping                Landscape & Hardscape
/remodels                   Pool Remodels
/maintenance                Weekly/Monthly Service
/outdoor-living             Kitchens, Pergolas, Fire/Water
/portfolio                  Photo gallery
/financing                  Payment plans
/about                      Story, values, service areas
/contact                    Lead form + contact info
/blog + /blog/:slug         Articles
/404                        Not found
```

This IA is solid and should carry over to Wix with one addition: `/dream-center` (or `/design-studio`) as a standalone interactive page so it can be deep-linked from ads and social.

---

## 4. Design System Audit

### 4.1 Summary
**Components reviewed:** 14 custom + 50 shadcn | **Issues found:** 23 | **Score: 74/100**

### 4.2 Design Tokens

| Category | Defined | Hardcoded instances found | Issue |
|---|---|---|---|
| **Colors** | 14 HSL vars (`--gold`, `--cream`, `--stone`, `--pool-blue`, `--pool-deep`, etc.) | 11 instances of raw `rgba(...)` in `Hero.tsx`, `PageHero.tsx` (gradient overlays, text) | Inline rgba breaks theming; should be tokens or Tailwind classes |
| **Typography** | 2 families, no explicit scale | Sizes set via arbitrary `text-[1.05rem]`, `text-[0.65rem]`, `text-[0.7rem]`, `text-[0.75rem]` in ~40 places | Needs a named scale (xs/sm/body/lg/display) for consistency in Wix |
| **Spacing** | Tailwind default | `py-24`, `py-32`, `py-20`, `py-28`, `py-16` mixed across sections | Pick two section rhythms (e.g., 80/120 px) |
| **Radius** | `--radius: 0.25rem` | Forms override with `rounded-none` | Deliberate editorial choice — keep, but document |
| **Shadows** | Only `hover:shadow-lg` used | No elevation system | Add 3-step elevation scale for cards/modals |
| **Motion** | Framer Motion everywhere | No `prefers-reduced-motion` guard | Accessibility issue (see §5) |

### 4.3 Color Palette (recommended Wix tokens)

| Token | HSL | Hex | Role |
|---|---|---|---|
| `cream` | 37 33% 96% | **#F7F1E8** | Page background, editorial sections |
| `stone` | 30 10% 9% | **#1A1814** | Body text, deep footer |
| `slate` | 30 6% 16% | **#2B2723** | Secondary dark, buttons |
| `gold` | 37 42% 61% | **#C9A464** | Primary accent, CTAs |
| `gold-light` | 37 55% 80% | **#E5CB9A** | Hero highlights, hover |
| `gold-dark` | 40 75% 31% | **#8B6914** | Focus ring, high-contrast text on cream |
| `pool-blue` | 196 66% 32% | **#1C738A** | Hero gradient, section accent |
| `pool-deep` | 203 62% 13% | **#0C2736** | Hero gradient base, footer alt |
| `mist` | 25 4% 52% | **#888278** | Muted body, captions |

**Contrast reality check (AA requires 4.5:1 for body text, 3:1 for large text):**
- ❌ Gold `#C9A464` on cream `#F7F1E8` = **2.2:1** — currently used for eyebrows and tiny uppercase labels all over the site. **Fails.** Use `gold-dark #8B6914` for any gold text on cream.
- ❌ `text-stone/60` (60% opacity black-ish) on cream ≈ **3.6:1** — passes for large text only. Any body copy at this opacity fails.
- ✅ Stone `#1A1814` on cream = 14:1. Use for all long-form copy.
- ✅ Cream on stone footer = 14:1.
- ⚠️ White `rgba(255,255,255,0.75)` subline over the pool-blue hero gradient: ratio depends on photo content. **Add a solid dark scrim behind the text block (not the whole image) to guarantee 4.5:1.**

### 4.4 Typography Scale (proposed, use in Wix "Theme Styles")

| Token | Family | Size / LH | Tracking | Use |
|---|---|---|---|---|
| `display-xl` | Cormorant Garamond, 300 | 72/80 px | -0.01em | Home hero H1 |
| `display-lg` | Cormorant Garamond, 300 | 56/64 px | normal | Page heroes |
| `display-md` | Cormorant Garamond, 400 | 40/48 px | normal | Section headings |
| `display-sm` | Cormorant Garamond, 400 | 28/36 px | normal | Card titles |
| `body-lg` | Jost, 400 | 18/30 px | normal | Hero sublines, intro paragraphs |
| `body` | Jost, 400 | 16/26 px | normal | Default body |
| `body-sm` | Jost, 400 | 14/22 px | normal | Card descriptions |
| `eyebrow` | Jost, 500 | 11/16 px | 0.3em uppercase | Gold eyebrows |
| `button` | Jost, 600 | 12/16 px | 0.2em uppercase | CTAs |

### 4.5 Component Completeness

| Component | States | Variants | A11y | Docs | Score |
|---|---|---|---|---|---|
| Hero (slider) | ✅ default | 1 | ⚠️ no pause control, motion not guarded | ❌ | 5/10 |
| PageHero | ✅ | 1 | ⚠️ contrast on subtitle | ❌ | 7/10 |
| DreamCenter cards | ✅ hover | 1 | ⚠️ link has no visible focus ring | ❌ | 6/10 |
| Services cards | ✅ hover | 1 | ⚠️ same as above | ❌ | 6/10 |
| Navigation | ✅ hover, open/close | mobile + desktop | ⚠️ dropdown not keyboard-navigable (onClick only) | ❌ | 5/10 |
| LeadForm | ✅ default, submitted | 1 | ✅ labels present, ⚠️ no error live-region | ⚠️ | 8/10 |
| CTASection | ✅ | 1 | ✅ | ❌ | 8/10 |
| Footer | ✅ | 1 | ✅ | ❌ | 9/10 |
| Testimonials | ✅ | 1 | ✅ | ❌ | 7/10 |
| Portfolio | ✅ | 1 | ⚠️ gallery needs alt text detail | ❌ | 7/10 |

### 4.6 Naming & Convention Issues

| Issue | Where | Recommendation |
|---|---|---|
| Inline `style={{ background: "linear-gradient..." }}` | `Hero.tsx`, `PageHero.tsx` | Move to Tailwind custom utility `bg-hero-gradient` or a Wix theme setting. Needed so Wix editors can't accidentally break it. |
| Mixed opacity text (`text-stone/60`, `text-cream/50`, `text-foreground/80`) | 30+ instances | Replace with named `text-muted`, `text-subtle`, `text-caption` tokens |
| Service route names vary (`/custom-pools`, `/remodels` vs. `/outdoor-living`) | `App.tsx` | OK — keep slugs but align on noun vs. action in nav labels |
| "ARISE & CO." in nav, "Arise Pools & Landscaping" in footer | | Pick one: **"ARISE & CO."** for luxury mark, full name for legal/SEO. Already consistent in current build, just document it. |

---

## 5. Accessibility Review (WCAG 2.1 AA)

Full `/design:accessibility-review` pass. Issues are grouped by severity.

### 5.1 Critical (must fix before launch)

| # | Issue | WCAG | Where | Fix |
|---|---|---|---|---|
| A1 | Gold text `#C9A464` on cream `#F7F1E8` fails 4.5:1 | 1.4.3 | Every `text-gold` eyebrow, nav hover, CTA label on light BG | Use `gold-dark #8B6914` for text on cream. Keep `gold` for dividers, icons >24px, and text on dark backgrounds only. |
| A2 | Hero subline `rgba(255,255,255,0.75)` over photo | 1.4.3 | `Hero.tsx`, `PageHero.tsx` | Raise to `0.92` and add a semi-opaque dark scrim (60% stone) behind the text column only. |
| A3 | Services dropdown opens on click, not keyboard-accessible, no ARIA | 2.1.1, 4.1.2 | `Navigation.tsx` | Use Radix `NavigationMenu` (already in deps) with `aria-expanded`, Esc-to-close, arrow-key nav. In Wix, use the native Dropdown element which is keyboard-accessible by default. |
| A4 | Hero slider auto-advances every 5.5s with no pause/stop control | 2.2.2 | `Hero.tsx` | Add pause button + respect `prefers-reduced-motion` to disable auto-advance. Also pause on hover/focus. |
| A5 | No visible focus styles on interactive elements | 2.4.7 | All buttons, links, cards | Add `focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gold-dark`. |
| A6 | `framer-motion` animates on scroll for every section | 2.3.3 | `Services`, `DreamCenter`, `About`, etc. | Wrap animations in `useReducedMotion()` or conditional `initial/animate`. |
| A7 | Social/contact icon links have no accessible name | 4.1.2 | `Footer.tsx`, `ContactPage.tsx` | Each `<a>` wraps text so this mostly passes — but the icon-only dot-indicators in hero have `aria-label` — good. Audit every icon-only button. |

### 5.2 Serious

| # | Issue | WCAG | Fix |
|---|---|---|---|
| A8 | Hero images are `loading="eager"` on all slides | 2.4.8 | Only first eager; rest lazy. Already partially done. |
| A9 | Form errors not announced to screen readers | 3.3.1, 4.1.3 | Add `role="alert"` or `aria-live="polite"` region; shadcn `FormMessage` is already ARIA-connected — verify after Wix port. |
| A10 | `<em>` used for visual italics in hero | 1.3.1 | Wrap accented word in `<span className="italic">` instead of `<em>` — `<em>` implies stress emphasis semantically. |
| A11 | 24px touch targets (toast close, nav dots) under 44×44 | 2.5.5 | Wrap with padded hit-area. |
| A12 | Alt text is generic (`alt={slide.headline}`) | 1.1.1 | Write descriptive alt for each image: e.g., "Backyard pool with travertine deck and fire bowls at dusk." |
| A13 | Text over gradient on portfolio cards may fail | 1.4.11 | Test each card; use the established dark-scrim pattern. |

### 5.3 Advisory / best-practice

- A14. Add `skip to content` link at top of `<body>`.
- A15. Declare page `<main>` landmark — shadcn layouts sometimes omit this.
- A16. Blog post pages should use `<article>` with `<header>` and published `<time>`.
- A17. Add `prefers-color-scheme` response (brand is warm-light, but at minimum avoid flash of white).
- A18. Provide transcripts/captions for any video — none currently, but planned Dream Center may include video backgrounds.

**Target: 0 Critical, 0 Serious issues before going live.**

---

## 6. Content & Messaging Audit

**Voice on current prototype:** aspirational, restrained, confident — this is correct for luxury. Keep it.

**Recommended tightening:**

| Page | Current weak spot | Upgrade |
|---|---|---|
| Home hero | "Build Your Dream Escape" + generic subline | Lead with a specific outcome: *"The backyard you see in magazines — built in your yard, on your calendar."* |
| About | "Founded in Gilbert, Arizona, Arise Pools..." | Add the founder's origin story in 2–3 sentences. Luxury buyers want to meet the principal. |
| Custom Pools | Process is described but not priced | Add a "typical investment range" bracket ($85k / $150k / $275k+ signature) — discerning buyers self-qualify. |
| Contact | "We'll be in touch within 24 hours" | Set a specific expectation: *"A designer — not a salesperson — will call you within one business day."* |
| Testimonials | Need specific names + projects | Replace generic stars with 3–4 signed testimonials; ideally with hero-quality photo of *their* pool. |

**Words to cut** (they dilute luxury): "affordable," "best," "competitive rates," "cheap." **Words to keep**: "commissioned," "signature," "designer," "heirloom," "bespoke," "complimentary consultation."

---

## 7. Performance Audit

Rough estimated Lighthouse scores for the prototype if deployed as-is:
- Performance: ~68
- Accessibility: ~78
- Best Practices: ~92
- SEO: ~98

**Perf wins for the Wix rebuild:**

1. **Images.** 7 hero-class JPEGs in `public/images/` and `public/images/client/`. In Wix, upload originals and let Wix's Media Manager auto-serve WebP + correct srcset. Target <200 KB per above-fold image.
2. **Fonts.** Move from `@import` Google Fonts (render-blocking) to Wix Theme → Custom Fonts with `font-display: swap` and preload for the two families only.
3. **Animations.** Wix Studio's built-in scroll effects render via GPU-accelerated CSS; prefer those over a JS motion library for sections outside the Dream Center.
4. **Hero slider.** 3-slide autoplay is expensive. Either (a) ship 1 hero image + subtle Ken Burns, or (b) preload slide 2 only, load 3 on idle.
5. **LCP.** Target <2.5s. Biggest lever: hero image width (1600 px is enough; don't ship 4K).

---

## 8. SEO Audit

`index.html` already ships **LocalBusiness schema** with aggregate rating and ROC licenses — excellent.

**Add when rebuilding in Wix:**

- `Service` schema for each of the 6 services under the business.
- `FAQPage` schema on Custom Pools and Financing pages.
- `Review` schema tied to 3–5 named testimonials.
- City landing pages: `/pools/gilbert`, `/pools/chandler`, `/pools/scottsdale` — high-intent "pool builder [city]" queries.
- H1 on every page (not all pages currently have one — check Blog index).
- Open Graph image updated to a vertical 1200×630 with a gold logo watermark.

---

## 9. Wix Rebuild Plan

### 9.1 Platform choice: **Wix Studio** (not Editor X or Classic)

Reasons:
- Full responsive grid (matches the 1200/1400 max-widths in the prototype).
- Velo (now called **Wix Code / Velox**) for the Dream Center configurator.
- CMS Collections for Portfolio, Blog, Testimonials.
- Theme Studio for the tokens in §4.

### 9.2 Page-by-page mapping

| Prototype route | Wix page | Wix building blocks | CMS? |
|---|---|---|---|
| `/` | Home | Section: Hero (Wix Video/Image Strip) → Dream Center (custom Velo component) → Services (Repeater) → Testimonials (Slideshow bound to CMS) → CTA Strip → Footer | Yes (Testimonials, Services) |
| `/custom-pools` | Custom Pools | Page Hero → Intro → Pool Types Gallery (Pro Gallery) → Process timeline → FAQ (Accordion) → CTA | — |
| `/landscaping` | Landscaping | Same pattern | — |
| `/remodels` | Pool Remodels | Before/After slider (Wix native) → Process → CTA | — |
| `/maintenance` | Maintenance | Plans comparison (Repeater with pricing) → CTA | — |
| `/outdoor-living` | Outdoor Living | Feature grid → Gallery → CTA | — |
| `/portfolio` | Portfolio | Pro Gallery bound to CMS (tags: pools/landscape/hardscape) | Yes |
| `/financing` | Financing | Calculator embed (third-party) + FAQ | — |
| `/about` | About | Story → Values → Team → Service areas map (Wix Google Maps) | — |
| `/contact` | Contact | Wix Forms + Google Map + contact info | — |
| `/blog` | Blog | Wix Blog app, custom category nav | Yes |
| `/dream-center` | **NEW** Dream Center | Full-page interactive configurator — see §10 | Yes (Saves submissions to a `DreamSubmissions` collection) |

### 9.3 Wix Theme Studio — paste-ready values

**Colors (Site Settings → Color Palette):**
```
Main 1 (Primary)   #1A1814   Stone
Main 2 (Accent)    #C9A464   Gold
Main 3 (Secondary) #2B2723   Slate
Main 4 (Accent 2)  #E5CB9A   Gold Light
Main 5             #1C738A   Pool Blue
BG                 #F7F1E8   Cream
```

**Typography (Theme → Custom fonts):**
- Headings: Cormorant Garamond, weights 300/400/400-italic
- Paragraphs: Jost, weights 300/400/500/600
- Apply the scale in §4.4

### 9.4 CMS Collections to create

1. **Portfolio** — `title`, `category` (ref), `description`, `heroImage`, `gallery`, `client` (optional), `yearCompleted`, `slug`
2. **PortfolioCategory** — `name`, `slug`
3. **Testimonials** — `authorName`, `location`, `quote`, `rating`, `photo`, `projectRef`
4. **BlogPosts** — use the Wix Blog app; map the prototype's `src/data/blogPosts.ts` into it
5. **DreamSubmissions** — `submittedAt`, `name`, `email`, `phone`, `selections` (JSON), `budgetRange`, `timeline`, `notes`, `source` (UTM)
6. **Services** — `title`, `icon`, `shortDesc`, `slug`, `heroImage` (so the home Services grid is editable by the client)

### 9.5 Integrations

- **CRM:** HubSpot (most likely) or Jobber/HCSS for trades. Lead form + Dream Center submit → webhook → CRM. Velo code: `fetch()` from a backend `.jsw` file to keep API keys server-side.
- **Booking:** Wix Bookings for the consultation calendar — gated on "Schedule My Dream Review" button at end of the configurator.
- **Analytics:** GA4 + Meta Pixel + Microsoft Clarity (for heatmaps on the Dream Center funnel).
- **Reviews:** Embed Google Reviews widget on Testimonials strip; keep the CMS version for layout control.

### 9.6 Redirects

Map every existing arisepal.com URL to the new structure in Wix URL Redirect Manager. Test 20 random old URLs before DNS cutover.

---

## 10. The Dream Center — interactive configurator spec

> This is the headline feature. Treat it as a product, not a section.

### 10.1 Problem

Luxury buyers want to **visualize and shape** before they talk to a salesperson. The current static card grid loses them at the first click. A configurator (a) qualifies leads, (b) captures intent with richer data, (c) doubles as a lead magnet.

### 10.2 User flow

```
Start screen
   │
   ▼
Step 1 — Project type   (single select: Pool · Landscape · Full Backyard · Remodel · Maintenance)
   │
   ▼
Step 2 — Pool style      (visual gallery: Geometric · Freeform · Infinity · Plunge · Custom)
   │
   ▼
Step 3 — Add features    (multi-select chips: Spa · Tanning Ledge · Fire Bowl · Waterfall · Grotto · LED · Swim-up Bar)
   │
   ▼
Step 4 — Landscape add-ons (multi-select: Turf · Pavers · Pergola · Outdoor Kitchen · Lighting · Privacy Wall)
   │
   ▼
Step 5 — Size & lot      (slider: small/medium/large; lot photo upload optional)
   │
   ▼
Step 6 — Budget & timeline  (investment range + preferred start window)
   │
   ▼
Step 7 — Your details    (name, email, phone, address)
   │
   ▼
Summary screen
   ├── Live visual preview (photo collage of closest match from portfolio CMS)
   ├── Estimated investment band ("Projects like yours typically invest $125k–$175k")
   ├── "Download My Dream Brief" (PDF auto-generated)
   └── "Schedule My Dream Review" (Wix Bookings)
```

### 10.3 Component spec

| Component | Purpose | Notes |
|---|---|---|
| `StepIndicator` | Horizontal progress with step labels | 7 dots + current step name; clickable backward only |
| `ChoiceCard` | Large tappable card with image + label + description | Selected state: gold border + check badge |
| `ChipGroup` | Multi-select pills for add-ons | Inline; each chip = icon + label |
| `MatchPreview` | Pulls closest Portfolio entry by tag match | Lazy-loads Pro Gallery image |
| `EstimateBand` | Shows investment range | Tied to a simple scoring rubric (see 10.5) |
| `Summary` | Reviews all selections with edit links | Inline edit jumps back to the step |
| `PDFExport` | Client-side generation of a branded brief | Use `jsPDF` or Velo backend with a template |
| `DreamSubmitButton` | Saves to CMS, fires webhook, routes to booking | Show loading + success toast |

### 10.4 Visual design

- **Full-bleed background** — subtle 2% grain texture over `cream`; at edges, a slow-rotating gradient from `pool-deep` → `pool-blue` behind a glass card.
- **Main card** — white, 16 px radius, `0 24px 60px -20px rgba(12,39,54,0.25)` shadow, 640 px max width on mobile, 960 px on desktop.
- **Typography** — display headings in Cormorant italic, step count in gold eyebrow style.
- **Transitions** — 320ms ease-out cross-fades between steps; respect `prefers-reduced-motion`.
- **Imagery** — each choice card shows a real portfolio photo, not an icon. Icons are for chips only.

### 10.5 Scoring & estimate rubric (simplified)

```
Base by project type:
  Pool new construction:     $85,000
  Pool remodel:              $28,000
  Landscape only:            $18,000
  Full backyard:             $145,000
  Maintenance plan:          $0 (route to Maintenance page instead)

Pool style multiplier:
  Geometric:  1.0
  Freeform:   1.15
  Infinity:   1.35
  Plunge:     0.7
  Custom:     1.25

Feature adders ($):
  Spa +$18k, Tanning ledge +$6k, Fire bowl +$4.5k ea,
  Waterfall +$12k, Grotto +$22k, LED lighting +$3.8k,
  Swim-up bar +$9k

Landscape adders ($):
  Turf (per 500sf) +$4.5k, Paver patio (per 300sf) +$7.5k,
  Pergola +$14k, Outdoor kitchen +$32k, Lighting pkg +$5.5k,
  Privacy wall +$11k

Size multiplier:
  Small (<1/4 acre): 0.9
  Medium: 1.0
  Large (>1/2 acre): 1.25

Round to the nearest $5k and show as a range: [estimate × 0.9, estimate × 1.2]
```

Keep the rubric in a Velo backend file so it's editable without a code change.

### 10.6 Data that goes to the CRM

```json
{
  "submittedAt": "2026-04-15T14:32:11Z",
  "contact": { "name": "...", "email": "...", "phone": "...", "address": "..." },
  "project": {
    "type": "full_backyard",
    "poolStyle": "infinity",
    "features": ["spa", "fire_bowl_x2", "led"],
    "landscape": ["pergola", "outdoor_kitchen"],
    "size": "medium"
  },
  "budget": "150k-200k",
  "timeline": "Q3_2026",
  "estimate": { "low": 165000, "high": 220000 },
  "matchedPortfolio": "pool-125",
  "utm": { "source": "...", "medium": "...", "campaign": "..." }
}
```

### 10.7 Accessibility requirements for the configurator

- All steps keyboard-navigable (Tab/Shift-Tab/Enter/Arrows).
- Each step has a named region + step heading that moves focus on transition.
- Motion guarded by `prefers-reduced-motion`.
- Choice cards implemented as `<label><input type="radio"></label>` (radios not buttons).
- Chip group uses `role="group"` with `aria-labelledby`.
- Summary uses a `<dl>` with dt/dd pairs.

### 10.8 Success metrics (review at 30/60/90 days)

- Start → finish completion rate — **target 35%**
- Finish → booking conversion — **target 22%**
- Avg time-on-page — **target 3–4 min**
- Qualified lead share (budget ≥ $75k) — **target ≥ 55%**

---

## 11. Luxury Elevation Checklist

The prototype gets many things right. These are the moves that push it from "premium" to "magazine-worthy":

1. **Photography is 80% of the feel.** Budget a half-day shoot with a professional who has architecture/hospitality credits. Twilight shots with pool lighting on > sunny midday shots.
2. **Anchor the hero on a named project**, not a stock tagline. "The Anderson Residence. Gilbert, AZ. Completed Spring 2026."
3. **Silence is luxury.** Increase section padding to 120 px desktop / 72 px mobile. Reduce visual elements per viewport by ~30%.
4. **Editorial grid with vertical asymmetry** on service pages — image left 7/12, text right 5/12, ample negative space.
5. **Remove all emoji and exclamation points** from CTAs and copy.
6. **One gold per viewport.** Too many gold accents cheapens; reserve for the single most important thing on screen.
7. **Signature motion** — one deliberate moment per page (e.g., hero image scale-in on load, section transition). Not every element.
8. **Client names matter.** "Built for the Harrison family, Paradise Valley." Ask for permission, offer them a free maintenance quarter in exchange.
9. **A printed look-book** (offered as PDF download and physical mail-out). The Dream Center's PDF export seeds this.
10. **Press / recognition bar** — if the client has any media mentions, association memberships (APSP, NPC), or award nominations, put them under the hero in a thin grayscale strip.

---

## 12. Content collection list (ask the client for these)

1. High-res photography of 10–15 completed projects (hero shot + 4–6 detail shots each).
2. 3–5 signed testimonial quotes with author names, cities, and ideally a photo of their project.
3. Founder bio (150 words) + professional headshot.
4. Team photos (group and individual) — optional but strong.
5. Copy of ROC licenses, insurance certificates (for a credentials footer).
6. Any press mentions, awards, association memberships.
7. Confirmed service-area list and pricing bands per service.
8. Maintenance plan pricing (if public).
9. Financing partner logos (and their disclosures).
10. Social handles once active.

---

## 13. Build schedule (suggested)

| Week | Deliverable |
|---|---|
| 1 | Content collection, photo shoot scheduled, Wix Studio site provisioned, theme tokens applied |
| 2 | Home, About, Contact pages built in Wix Studio + CMS collections created |
| 3 | 6 service pages + Portfolio (CMS-backed) + Blog migrated |
| 4 | Dream Center configurator v1 (Velo) — steps 1–7 + CMS save |
| 5 | Dream Center v1.5 — PDF export, portfolio match, CRM webhook |
| 6 | Accessibility pass, performance tuning, redirects, staging QA |
| 7 | Client review + revision round |
| 8 | Launch + 30-day post-launch analytics review |

---

## 14. Priority actions (do these first)

1. **Fix gold-on-cream contrast** globally — one token swap, unlocks AA compliance.
2. **Rebuild Dream Center as a configurator** (§10) — this is the single biggest conversion lever.
3. **Schedule twilight photography** of 3 signature projects — luxury lives or dies on the hero imagery.
4. **Provision Wix Studio**, apply the theme tokens in §9.3, and create the CMS collections in §9.4.
5. **Write the keyboard-nav spec** (§5.1 + 10.7) into the Wix dev handoff so accessibility isn't an afterthought.

---

*End of report.*
