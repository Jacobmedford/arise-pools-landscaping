# Arise Pools & Landscaping site audit, 10-16-26

Scope: /Users/jakemedford/arise-pools-landscaping, live at https://www.arisepal.com. Read-only. No edits, commits, pushes or deploys.

## How this was run

- Audited git HEAD (a8b8692), extracted with `git archive` to a scratch folder. Live HTML is byte-identical to HEAD for all 62 deployed pages (check 9), so HEAD is the truth for what customers see.
- 62 deployed .html pages (excludes the .vercelignore list). Python scripts covered all 10 checks. About 80 HTTP requests to arisepal.com, plus one CORS OPTIONS preflight to the n8n lead webhook (no lead data sent, no POST).
- NOTE: another session is editing the working tree right now (uncommitted: contact.html, index.html, oasis.html, data/projects.json, js/portfolio-gallery.js, scripts/projects-sync.py, new js/lead-survey.js, css/lead-survey.css, ~280 new project photos). It replaces the /contact and /oasis forms with a shared "lead survey". Findings below are about HEAD / live. A short WIP note is at the end.

## Result at a glance

Clean (no findings): broken internal links (3,208 links checked, 0 broken), missing images/CSS/JS (0), GA4 `G-FLPRD1LYFH` is the first thing in `<head>` on all 62 pages with exactly one `gtag('config')`, one canonical per page matching its URL, unique titles and descriptions, JSON-LD parses on all 61 pages that have it, phone is `(623) 292-3073` / `tel:+16232923073` everywhere (0 wrong numbers), only `inquiry@arisepal.com` as a real email, no brand other than Pentair, viewport meta on all 62 pages, no inline fixed widths over 400px, all 60 sitemap URLs return 200.

---

## CRITICAL

None that take the site down or break navigation. The closest items are the legal and trust risks at the top of High (H1, H2) and the silent lead loss in H3.

---

## HIGH

### H1. Unverified / likely fabricated credentials, awards and reviews shown as fact
Legal and trust exposure (FTC endorsement rules, BBB logo/claim misuse, false advertising). Nothing in the repo substantiates any of these. The portfolio only documents 5 projects.

- `index.html:137-141`, `about.html:115-119`, `press.html:108-112`, `oasis.html:351-352`: trust bar "BBB A+ Rated", "NPC Member", "5.0 Google Rating / 5-Star Google", "200+ Projects Delivered".
- `press.html:99-102`: "Phoenix Home & Garden" feature ("The New Desert Modern Backyard", "Arise infinity-edge build in Paradise Valley"), "AZ Big Media ... top outdoor design-build firms for 2025", "Ranking Arizona ... reader vote", "Local First Arizona" membership.
- `reviews.html:97-135` and the homepage Client Stories block (`index.html`, "What Our Clients Say"): six five-star testimonials from "Michael & Sarah H., Gilbert", "David & Jennifer T., Scottsdale", "Robert & Lisa M., Paradise Valley", "Chris & Amanda R., Queen Creek", "James & Nicole P., Chandler", "Daniel & Karen W., Mesa" plus "5.0 on Google". Reads like template copy. Only Gilbert and the Superstition/San Tan/Gold Canyon projects exist in the portfolio.
- `cities/scottsdale.html:103`: "Arise has completed over 40 projects across Scottsdale". `cities/gilbert.html:102`: "we have transformed more Gilbert backyards than any other city". No Scottsdale project exists in `data/projects.json`.
- `index.html`/`about.html`/`oasis.html`: "15+ years" (60 pages say "15 years"), "lifetime of Arise support" (`process.html`, `about.html`, `index.html`).

Fix: Jake confirms each claim with proof (BBB profile URL, Google Business Profile rating and review count, press clippings, real signed testimonials with permission). Anything not proven gets removed or replaced with verifiable facts (ROC numbers, real project count, real review excerpts linked to the Google profile). Remove the `press.html` Recognition block entirely until proven. Replace testimonial names with real approved ones or delete the section.

### H2. Privacy, Terms and Accessibility pages literally say "placeholder language"
- `privacy.html:98`, `terms.html:97`, `accessibility-statement.html:97`: visible text "Last updated: May 2026. This is placeholder language, replace with your finalized policy before launch." . Live right now.
- All three have no `<h1>` (h1 count 0), 40 to 61 character meta descriptions, and the policy is ~5 sentences. Privacy policy does not mention Google Analytics, SMS/phone contact, or the third-party processors (GHL, n8n, Google Sheets) that receive form data.

Fix: replace with real policies (include analytics, SMS consent + STOP/HELP language for A2P, data processors, contact email). Delete the "placeholder language" sentence. Add one `<h1>` per page.

### H3. Dream Center (/configurator) swallows lead-capture failures and shows success anyway
- `configurator.html:1315`: success panel appears via `setTimeout(..., 1500)` regardless of the webhook result.
- `configurator.html:1403-1412`: `fetch(N8N_WEBHOOK ...)` result is only `console.error`'d. A 4xx/5xx, network drop or CORS block loses the lead while the visitor sees "Thank you".
- Compounding factor, see H4: the n8n webhook only allows CORS from `https://www.arisepal.com`.

Fix: make `fireGHLWebhook()` return the promise; show the success panel only on `res.ok`; on failure show an error with `(623) 292-3073`; retry once; optionally dual-post to the GHL webhook like /oasis does.

### H4. Apex domain serves the site (200) instead of redirecting to www, and CORS breaks forms there
- `curl -I https://arisepal.com/` returns 200, not a 301 to `https://www.arisepal.com/` (also `http://arisepal.com/contact` redirects to `https://arisepal.com/contact`, still apex). Canonicals point to www so SEO damage is limited, but duplicate indexing and split GA sessions are possible.
- The n8n webhook `https://jacobmed.app.n8n.cloud/webhook/ariseleadcapture` answers preflight with `access-control-allow-origin: https://www.arisepal.com` only. A visitor on the apex domain submitting /contact, /guide or /configurator is blocked by CORS. /contact and /guide show the error message; /configurator shows success (H3) and loses the lead.

Fix: in Vercel, set `arisepal.com` to redirect (308) to `www.arisepal.com`. Optionally also add the apex origin to the n8n webhook CORS allow-list.

### H5. Financing page quotes a payment with no APR or lender disclosure
- `financing.html:104`: "From $612/mo on an $85,000 project, 180 months, approved credit". Advertising a payment amount and term without APR, finance charge and lender terms is a Truth in Lending (Reg Z) trigger-term problem. "Home Improvement Loans" is named as the partner with no link or legal text.

Fix: add APR, "subject to credit approval", lender name and NMLS/licence if applicable, and a link to the lender terms, or remove the dollar figure.

---

## MEDIUM

### M1. Consent language missing on /contact, /guide and /configurator
Only `oasis.html:482` has the TCPA-style line ("may call, text or email you ... Reply STOP"). `contact.html:99-118`, `guide.html:99-111` and the entire `configurator.html` collect name, phone, email (configurator also street address) with no consent text and no privacy link. `configurator.html` has no link to `/privacy` at all (0 matches), no site nav, no footer, no phone number and no ROC info.
Fix: add the same consent paragraph and `/privacy` link under each submit button, and a minimal header/footer with the phone to the configurator.

### M2. /guide promises a guide that is never delivered
`guide.html:99-111` ("Send Me the Playbook") reuses `#contactForm` and `site.js`. On success the user sees "Thank you, your message is on its way. We'll be in touch within one business day." There is no PDF in the repo (`find . -name '*.pdf'` returns nothing) and no download or email step on the page. The lead lands in the same n8n flow tagged `source: 'contact-page'`, `tags: 'Website Contact Form'`, distinguishable only by `service_type = "Guide Download"` (hidden field `guide.html:106`).
Fix: either show a direct download link on success or tell the visitor the guide is emailed; send `source: 'guide-page'` and tag `Guide Download` (read from a `data-source` attribute on the form).

### M3. /contact and /guide forms: no spam protection, weak validation, a11y gaps
- `contact.html:99-118`, `guide.html:99-111`: no honeypot, no time check, no captcha. `/oasis` has a honeypot (`oasis.html:475`), so the three n8n forms are the soft target. `/configurator` also has none.
- `site.js:83-91` treats any resolved `fetch` as success (`.then(function (res) {...})` never checks `res.ok`), so an n8n 4xx/5xx shows "Thank you". Fix: `if (!res.ok) throw new Error(res.status)`.
- Labels are not associated with inputs (6 `<label>` without `for` on contact, 4 on guide, 10 on configurator). Phone input placeholder is the business number `(623) 292-3073` (`contact.html:105`, `guide.html:105`, `configurator.html:906`), which looks pre-filled and confuses users. Use `(555) 555-5555` or none.
- Success copy in `site.js:90` uses an em-dash; swap for a comma when next touched.

### M4. Missing 404 page, favicon.ico, and security headers
- `https://www.arisepal.com/zz-not-a-page-404test` returns Vercel's bare text "The page could not be found / NOT_FOUND". No `404.html` in repo. `/favicon.ico` returns 404.
- `vercel.json` only sets cache headers. No `X-Frame-Options`/CSP `frame-ancestors`, `X-Content-Type-Options`, `Referrer-Policy`, `Permissions-Policy`.
Fix: add `404.html` using the site nav/footer, add a `favicon.ico` (copy of the 32px PNG converted) and a `headers` block for the global security headers.

### M5. Unsubstantiated/stale boilerplate on service and city pages (thin, templated content)
- 8 service pages share 5 of 7 paragraphs verbatim (e.g. "Geometric, freeform, infinity edge, and plunge pools..." appears on 10 pages); 8 service sub-pages are ~80 words each with the same text pattern ("Every freeform pools project from Arise is custom-engineered..." has a grammar bug from token substitution: `services/custom-pools/freeform.html`, `geometric.html`, `plunge-pools.html`, `spa-integration.html` etc.).
- 11 city pages (`cities/*.html`) are 96 to 143 words each, 33% of paragraphs shared, word-sequence similarity 37% to 50% between pairs. Thin for local SEO.
- "Schedule a complimentary design consultation and discover what's possible in your backyard." appears on 42 pages (CTA block, fine) and "Use our Dream Center..." on 11 city pages.
Fix: give each city page 300+ words of real local content (named neighborhoods, HOA/permit specifics, a real project from the portfolio), consolidate or expand the sub-service pages, fix the singular/plural substitution.

### M6. Sitemap and robots details
- `sitemap.xml` has 60 URLs with no `<lastmod>`. Blog posts have dates; add `<lastmod>`.
- Deployed but not in sitemap: `/oasis` (indexable, no robots meta; it is a paid landing page that duplicates homepage claims, so decide: add `noindex` or add to sitemap) and `/book` (correctly `noindex, follow`).
- `/data/projects.json` and `/data/content-rotation.json` are publicly served (200). They expose internal agent instructions and an internal path (`data/projects.json:2` mentions `ClaudeCode-Master/Clients/Arise Pool and Landscaping/CLAUDE.md`; `data/content-rotation.json` `_readme` describes the content agent and agent-reach workflow). Fix: add `data/` to `.vercelignore` (scripts read it locally; `js/portfolio-gallery.js` embeds its own copy).

### M7. Dead weight and privacy of unpublished photos
476 image files, 432 of them (about 209 MB of 224 MB) are not referenced by any deployed page, JS or JSON, e.g. most of `images-for-web-or-mls`, `-2`, `-3`. They are still publicly fetchable (immutable cache header) and can include unpublished or client photos. Fix: move unused raw photos out of the deployed tree or add them to `.vercelignore`.

### M8. Business info inconsistencies across pages
- Process says Discovery Call is "15 minutes" (`process.html:99`) while /oasis, /book and the homepage survey promise a "30-minute design call" (`book.html:14,68`).
- Contact page says "Gilbert, AZ (by appointment)" and "Saturday 9am - 2pm (by appointment)" (`contact.html:123,127`), while the footer on all 59 standard pages and the JSON-LD say Saturday 9 to 2 with no appointment caveat and "Gilbert, AZ 85295".
- Contact form service dropdown (`contact.html:109-111`) lists 6 options (Custom Pool, Pool Remodel, Landscape Design, Outdoor Living, Full Backyard, Maintenance) but nav/footer list 8 services; Hardscape & Sport Courts, Water & Fire Features, Smart Automation & Cleaning Systems are missing from the form.
- Footer phone `(623) 292-3073` is plain text, not a `tel:` link, on the 59 standard pages (`index.html:461` pattern; `oasis.html` footer is correct). Make it `<a href="tel:+16232923073">`.

### M9. Missing structured-data fields for local SEO
JSON-LD `HomeAndConstructionBusiness` (`index.html:34` and the 60 other pages) has `PostalAddress` with only region/country: no `addressLocality` ("Gilbert"), `postalCode` ("85295"), no `sameAs` (no GBP/social links exist anywhere on the site, zero external links), no `geo`. Good: no fabricated `aggregateRating`. Fix: add locality/zip, `sameAs` with the real Google Business Profile, Facebook, Instagram; add a footer link to the GBP.

---

## LOW

### L1. Head hygiene
- Meta descriptions: 26 of 62 are under 70 characters (e.g. `reviews.html` 41, `press.html` 41, `accessibility-statement.html` 40, `referral-program.html` 44, all 11 city pages 56 to 67); 12 are over 165 (blog posts, up to 210 on `blog/pool-permits-and-hoa-approval-in-scottsdale.html`). Titles over 65 characters on 12 pages, longest `blog/pool-builder-johnson-ranch-san-tan-valley-az.html` (101), `blog/custom-pool-builder-san-tan-valley-az.html` (91), `blog/arizona-backyard-shade-ramadas-and-pergolas.html` (89).
- `book.html` has no OG/Twitter tags and no JSON-LD (intentional for a noindex page; fine).
- `<meta charset>` sits after the GA block (`index.html:3-11`); still inside the first 1024 bytes so safe, but move charset first for hygiene.
- 57 pages load `/css/site.css` unversioned, 2 load `?v=20261008` (`index.html` and `portfolio.html`). CSS is cached `max-age=86400`; unversioned pages can serve stale CSS for up to a day after a deploy. Use one `?v=` constant everywhere.

### L2. Images
155 `<img>` tags: 0 missing `alt`, 1 intentionally empty; 100% lack `width`/`height` (layout shift risk, e.g. `blog.html:100-135`, `arise-logo-footer.png` in every footer); 81 non-first images lack `loading="lazy"` (worst: `blog.html` 12, `index.html` 12, `portfolio.html` 8, `services.html` 8). Images over 600 KB: `/images-for-web-or-mls-3/100-web-or-mls-DJI_20260415111249_0209_D.jpg` 928 KB (`portfolio.html`, `press.html`), `/images-for-web-or-mls-2/1-web-or-mls-DJI_20260408132347_0003_D.jpg` 841 KB (11 pages, also the og:image of 2 blog posts and the homepage hero), `.../1-web-or-mls-DJI_20260413181826_0067_D.jpg` 790 KB, `.../15-web-or-mls-DJI_20260413182421_0114_D.jpg` 661 KB, `.../40-web-or-mls-IMG_0673.jpg` 651 KB. Fix: re-export under 300 KB for hero/og use, set width/height, add lazy loading.

### L3. Accessibility and markup
- No `<main>` landmark and no skip link on any page.
- Heading level skips (h2 to h4) on 16 pages (about, careers, index, press, process, referral, services/*). `contact.html` goes h1 to h4.
- `privacy`, `terms`, `accessibility-statement` have no h1 (see H2).

### L4. Em-dashes
56 of 62 pages contain U+2014 (383 characters total). Highest: `configurator.html` 27, `blog/designing-for-monsoon-dust-and-115-degree-summers.html` 25, `blog/12-pool-shapes-for-arizona-lots-under-quarter-acre.html` 22, `blog/what-a-125k-pool-actually-gets-you-2026.html` 22, `blog/monsoon-pool-recovery-checklist.html` 19, `index.html` 12, `services/custom-pools.html` 11, `services/hardscape.html` 11. Includes titles like `index.html:12` (the homepage title uses a long dash between the brand and the tagline) and OG tags. Replace with commas/colons/pipes when each page is next touched. Do not mass-replace blindly inside JSON-LD without a parse check.

### L5. Stale or leaky strings
- `configurator.html:1311,1364` comments reference "a real Wix build" / "Wix Velo .jsw" (Wix is dead for this client). Comment only, not visible.
- `js/site.js:3` header comment says "contact to GHL" but the code posts to n8n.
- `oasis.html:537` embeds a full inline `var PROJECTS = [...]` copy of the project/photo data in addition to `js/portfolio-gallery.js` and `data/projects.json`; three copies can drift (the WIP session is touching all three).
- `configurator.html` displays dollar estimates computed client-side from hard-coded ranges (`calculateEstimate`, `configurator.html:1326`, e.g. custom pool $85k to $175k, maintenance $150 to $350/mo). These are customer-facing price promises. Confirm Jake approves the ranges and the page carries an "estimate only" disclaimer.
- `careers.html` advertises four open roles with no apply mechanism beyond "Get In Touch". Confirm the roles are real.
- `referral-program.html`: "$500 credit or a complimentary quarter of pool maintenance" with no terms. Confirm with the client and add terms.

### L6. Not bugs (checked and correct)
- /oasis posts to GHL webhook `eea6dd51-...` plus n8n `webhook/ariseoasis`, both-fail error path, honeypot, consent line, redirect to /book on success: correct and well built.
- /book embeds the GHL calendar widget (`book.html:90-108`), noindex: correct.
- Nav/footer: 59 of 62 pages are byte-for-byte consistent in nav, mobile drawer and footer link sets (all 8 service names identical, ROC# 342276/342277 line identical). The 3 variants (`oasis.html`, `book.html`, `configurator.html`) are minimal landing layouts by design; `configurator.html` has no header nav or footer at all (see M1).
- No lorem ipsum, TODO, "coming soon" or other placeholder text outside the policy pages in H2 (the only matches are `john@example.com`/`you@example.com` input placeholders).

---

## Check-by-check results

1. Links/assets: 3,208 `<a>` links, 155 `<img>`, CSS `url()`, scripts, og/twitter images and all 72 gallery photo URLs generated by `js/portfolio-gallery.js` resolve. 0 broken. `/#reviews` anchor exists (`index.html` id="reviews"). `/portfolio#slug` anchors accepted per instructions.
2. Head: GA4 first on 62 of 62, one canonical on 62 of 62, canonical equals URL on 62 of 62, 0 duplicate titles, 0 duplicate descriptions, OG+Twitter on 61 of 62 (`book.html` excluded, noindex), favicon + apple-touch on 62 of 62, JSON-LD valid on 61 (all blocks parse). Length issues in L1.
3. NAP: 0 wrong phones, 0 wrong emails, business name consistent, 21 Pentair mentions in 8 files and no other equipment brand (two generic "variable-speed pumps" mentions in `blog/monsoon-pool-recovery-checklist.html:157` and `blog/designing-for-monsoon-dust-and-115-degree-summers.html:131`, fine). Address is only "Gilbert, AZ 85295" (no street, intentional).
4. Nav/footer: see L6 and M8.
5. Content: see H1, H2, M5, L4. 56 of 62 pages have em-dashes.
6. Images: see L2.
7. Sitemap/robots: 60 URLs, all 200, no duplicates, no URLs without a page; `robots.txt` is `User-agent: * / Allow: / / Sitemap:` (sane). Gaps in M6.
8. Forms (HEAD):

| Page | Posts to | Required | Honeypot | Success state | Failure state |
|---|---|---|---|---|---|
| /contact (`contact.html:99`, `#contactForm`, handled by `js/site.js`) | n8n `webhook/ariseleadcapture` | first name, email, phone (JS-checked, `novalidate`) | none | text "Thank you..." | shown only on network exception, not on HTTP error (M3) |
| /guide (`guide.html:99`, same handler) | same n8n webhook | same | none | same message, no guide delivered (M2) | same |
| /configurator (7-step wizard, `configurator.html:1403`) | same n8n webhook | first/last name, email, phone, address, etc. | none | summary shown after fixed 1.5 s timer | none (console only), see H3 |
| /oasis (`oasis.html:451`, `#oasisForm`) | GHL `eea6dd51` + n8n `webhook/ariseoasis` | first, last, phone (10 digits), email | yes (`#f_company`) | redirect to /book | inline error with phone link, retries GHL once |
| /book | none (GHL calendar embed) | n/a | n/a | n/a | n/a |

9. Live: all 60 sitemap URLs plus /book and /oasis return 200 with 0 redirects; 62 of 62 live bodies are byte-identical to repo HEAD (titles match). Also: `robots.txt`, `sitemap.xml`, `/css/site.css`, `/js/site.js`, `/data/*.json` all 200; `/index.html` and `/contact.html` 308 to the clean URL (good); `http://www` 308 to https (good); `https://arisepal.com/` 200 with no redirect (H4); unknown path 404 with bare Vercel text (M4); `/favicon.ico` 404.
10. Mobile: viewport `width=device-width, initial-scale=1.0` on 62 of 62; no inline `width`/`min-width` over 400px in style attributes or `<style>` blocks; `css/site.css` only has `min-width: 768px` media queries and a `.contact-grid` mobile override (`site.css:1274-1276`); no mobile blockers found.

---

## Suggested fix order

1. H1 and H2 (remove or substantiate claims; real policies). Content decisions need Jake.
2. H3 + H4 (configurator success-on-failure; apex redirect). Small, high payoff for lead capture.
3. H5 financing disclosure.
4. M1 to M3 (consent, guide delivery, spam protection, `res.ok` check in `site.js`).
5. M4, M6 (404, favicon, headers, `.vercelignore` for `data/`), M7.
6. Remaining Medium/Low in any batch.

---

## FYI: uncommitted work in progress seen during the audit (not audited as shipped)

At ~14:35 the working tree differed from HEAD: `contact.html` and `oasis.html` forms replaced by `<div class="lead-survey">` fed by new `js/lead-survey.js`, `index.html` gained a homepage survey section, ~280 new project photos, `data/projects.json` + `js/portfolio-gallery.js` regenerated. Observations on `js/lead-survey.js`: has honeypot (`ls-hp`), consent line (matches oasis), dual-posts to GHL webhook `eea6dd51` + n8n `webhook/ariseoasis`, redirects to /book. Two things to watch when it ships: (a) /contact would then route to GHL + `ariseoasis` instead of `ariseleadcapture`, which departs from the routing described as correct, so confirm intent; (b) `guide.html` still uses the old `#contactForm` + `site.js` path, so M2/M3 stay open there. Untracked files must be committed together or the live pages will reference missing assets.
