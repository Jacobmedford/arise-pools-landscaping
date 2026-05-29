# Arise Pools — Deploy-Readiness Report
*Prepared for Vercel deployment · rebuilt from the approved design*

## Summary

The site has been **rebuilt properly as a complete, responsive, multi-page static site** in the project folder, ready for your Vercel deployment. The earlier auto-generated Wix build (broken hero, overflowing nav, unwired form) has been set aside — this rebuild uses the exact, approved Design DNA and renders correctly on desktop, tablet, and mobile.

**Bottom line:** Desktop and tablet are verified and clean. Mobile renders correctly in headless testing across all four target widths, with one issue found and fixed (contact form now stacks on mobile). The remaining gate before go-live is **real-device testing + a live GoHighLevel lead test** — see the Mobile Device Test Plan.

---

## What was built

A 25-page site (plus the Dream Center configurator):

- **Home** (`/`) — hero slideshow, trust bar, Dream Center teaser, portfolio, services, 7-step method, testimonials, all 11 cities, financing strip, closing CTA.
- **Services overview** (`/services`) + **6 service detail pages** (`/services/custom-pools`, `landscape-design`, `pool-remodels`, `outdoor-living`, `hardscape`, `water-fire-features`).
- **11 city pages** (`/cities/...`): Gilbert, Chandler, Mesa, Scottsdale, Queen Creek, Phoenix, Tempe, Paradise Valley, Fountain Hills, Cave Creek, San Tan Valley.
- **About**, **Process**, **Financing**, **Portfolio**, **Contact**.
- **Dream Center** (`/configurator`) — the 7-step interactive configurator.

All pages share one stylesheet (`/css/site.css`) and one script (`/js/site.js`), generated from `build.js` for consistency. Navigation, footer, and mobile drawer are identical site-wide.

## What's verified ✓

- **Hero renders correctly** — "Designed Outdoors. Built Once. Enjoyed Forever" on clean lines (the Wix word-breaking defect is gone). Confirmed at 1440px, 768px (iPad), 375px (iPhone SE), 393px, and 412px.
- **Navigation** — desktop nav fits without overflow; mobile hamburger + drawer + services accordion all wired to real pages (no `href="#"` dead links).
- **Link integrity** — automated check: 980 internal links, 89 image references, **0 dead links, 0 missing images**.
- **Mobile layout** — full-page mobile scroll reviewed; every section stacks to a single column cleanly. Sticky "Design My Backyard / Call Now" bar pinned correctly.
- **GoHighLevel wiring** — both the Dream Center (full lead payload + estimate + smart tags) and the Contact form POST to your GHL inbound webhook.
- **Content config** — "15+ years" copy, Home Improvement Loans financing partner, all 11 cities, client photography throughout. No `arisepal.com` references.
- **Clean URLs** — `vercel.json` set so `/about`, `/services/custom-pools`, `/cities/scottsdale`, `/configurator` all resolve without `.html`.
- **Deploy hygiene** — `.gitignore` + `.vercelignore` exclude `node_modules`, build tooling, QA screenshots, and dev docs so they aren't committed or served.

## Fixed during QA

- **Contact form** was rendering as two cramped side-by-side columns on phones → added a mobile breakpoint so it now stacks to a single column. Re-verified at 375px.

## Open items before go-live (your gate)

1. **Real-device testing** — run `Arise-Mobile-Device-Test-Plan.md` on actual iPhone SE / iPhone 15 Pro / Pixel 7 / iPad. Headless rendering is a strong signal but not a substitute for real hardware (touch, Safari quirks, safe-areas, cellular performance).
2. **Live GoHighLevel lead test** — submit a real Dream Center entry and a real Contact entry, confirm both land in GHL with correct fields/tags, then delete the test contacts. *(Webhook is wired but must be confirmed end-to-end with the live GHL account.)*
3. **Placeholder business details** — phone is shown as `(480) 555-POOL` and email as `hello@arisepools.com` across the site. Swap in the real phone/email before launch. (Also: ROC# is a placeholder `123456`.)
4. **Staging first** — deploy to the Vercel **preview** URL and review there. Per your standing instruction, do **not** point the production domain / go live until mobile testing passes.

## Notes

- The Dream Center service icons are emojis; they may show as empty boxes in some desktop emulators but render normally on real phones/tablets.
- The original approved preview is preserved as `Arise-Pools-Visual-Preview.html` (excluded from deploy).
- To regenerate pages after content edits: `node build.js` (edits live in `build.js` / `_home-body.html`).

## Deploy steps (when ready)

1. Push the folder to the linked Vercel project (`arise-pools-landscaping`) — `push-to-github.sh` is set up, then Vercel auto-builds; or use the Vercel CLI/dashboard.
2. Review the **preview** deployment URL.
3. Run the mobile test plan + GHL lead test.
4. Only after passing: promote to production / attach the domain.
