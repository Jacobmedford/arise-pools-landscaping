# Arise Pools & Landscaping: Off-Site SEO Plan (backlinks, citations, Google Business Profile)

Prepared 10-16-26. Read-only research. No accounts created, no forms submitted. Site audited separately in `ops/SITE-AUDIT-10-16-26.md`.

Check column legend used in every table:
- **V** = I loaded the URL this session (HTTP 200 or page text fetched).
- **S** = the site blocks automated checks (403/400/502) or I only saw the URL in a search result or as a link on a page I loaded. Open it in a normal browser.
- **U** = unverified. Treat as a lead, confirm before acting.

---

## 0. Read this first (findings that change the plan)

1. **A BBB profile for "Arise Pools & Landscaping" already exists, and its contact data does not match your NAP.** The BBB page (loaded this session) shows: city San Tan Valley, AZ 85140, phone (480) 234-8900, website arisepal.com, BBB Accredited since 12/21/2022, A+ rating, "Business Started 8/23/2022", "Years in Business 4", a linked Facebook profile (id 100087511008198). UPDATE 10-16-26: the owner confirmed San Tan Valley 85140 and (480) 234-8900 are correct, so BBB already matches; the website was switched to match. Two problems: (a) NAP mismatch will split citations and confuse Google; (b) "Years in Business 4" contradicts the "15+ years" on the site (audit item H1). Confirm this BBB record is yours, then fix the address, phone and hours with the local BBB, and reword "15+ years" to what is true for the company (for example "our team has 15+ years of experience" only if accurate). BBB profile: https://www.bbb.org/us/az/san-tan-valley/profile/commercial-landscape-contractors/arise-pools-landscaping-1126-1000105031 (V via reader, S for direct curl).
2. **Nothing else turned up for the brand.** Two web searches found no Google Maps, Yelp, Houzz or Instagram page named "Arise Pools & Landscaping" in Arizona. The site itself has zero external links and no `sameAs` (audit M9). Assume you are starting from near zero except BBB and that Facebook profile. Check Google Maps by hand for an auto-created listing before creating a new one (duplicates are a policy problem).
3. **Time-sensitive: Phoenix Home & Garden Readers' Choice nominations close October 25, 2026.** Page text: "Submit nominations October 1-25. Vote on Finalists November 1-30." Local Arizona businesses only. https://www.phgmag.com/2027-readers-choice-ballot/ (V).
4. **Time-sensitive: Maricopa County Home & Garden Show, January 15 to 17, 2027, Arizona State Fairgrounds.** Vendor application: https://maricopacountyhomeshows.com/become-a-vendor/ (V). Booth price is not published.
5. **Do not build link outreach on unproven claims.** The site's trust bar and `press.html` still show items the audit flagged as unsubstantiated (Google 5.0, "Phoenix Home & Garden" feature, AZ Big Media ranking, "Local First Arizona" membership, 200+ projects). Editors and BBB check these. Fix or remove them before pitching anyone. The FTC rule on fake reviews and testimonials is in Section 7.
6. **Two traps found while verifying.** `expressupdateusa.com` (the old Data Axle "Express Update" address) now redirects to an unrelated web design agency (hexxen.com): do not use it. `evp.org` redirects to a GoDaddy "for sale" page, so it is not the East Valley Partnership.
7. **Google retired public Q&A.** Do not plan a "seed the Q&A" tactic (Section 1.8).
8. **Tooling note.** Exa (the agent-reach search backend) rate-limited on its free tier, so research also used web search, direct page fetches and the Jina reader (agent-reach web channel).

### Canonical NAP (use this exact record everywhere)

| Field | Value | Note |
|---|---|---|
| Name | Arise Pools & Landscaping | No "LLC" unless it is on your signage (Google rule). No city or keywords in the name. |
| City, ZIP | San Tan Valley, AZ 85140 | Owner confirmed 10-16-26. Site and schema show city + ZIP only; GBP hides the address (service-area business). Yelp lists 85 W Combs Rd. |
| Phone | (480) 234-8900 | Same number on site, GBP, every directory. |
| Email | inquiry@arisepal.com | |
| Website | https://www.arisepal.com/ | Always `www` (apex domain does not redirect yet, audit H4). |
| Licenses | ROC# 342276 (Commercial), ROC# 342277 (Residential) | Check the ROC record matches (Section 2). |
| Hours | Decide once, copy everywhere | Site says Mon to Fri plus Sat 9 to 2 in the footer but "by appointment" on /contact (audit M8). |

---

## 1. Google Business Profile (GBP) checklist for a pool builder

All Google rules below were read from Google's own help pages this session (links inline, all V).

### 1.1 Eligibility and profile type (decide first)
- Google's rule: a business that serves customers at their homes and has no staffed, signed storefront is a **service-area business**, gets one profile, and should **hide the address** (https://support.google.com/business/answer/3038177 and https://support.google.com/business/answer/9157481).
- A **hybrid** profile (address shown plus service areas) requires permanent signage and that the location "should be staffed by your team and able to receive customers during its stated hours."
- Virtual offices, mailbox addresses and co-working desks without signage and staff are not eligible.
- **Decision for Arise:** if the Gilbert address is a home office or has no signage, use service-area business and clear the address. If there is a staffed, signed design studio, hybrid is allowed. Pick one and make the website, BBB and every citation say the same thing.
- Verify the profile before anything else; photos and many features only show after verification (https://support.google.com/business/answer/2911778).

### 1.2 Categories
Google: choose the primary category that best describes the core business and "the fewest number of categories it takes" for the rest; categories complete the sentence "This business IS a" (https://support.google.com/business/answer/7249669). Changing categories can trigger re-verification. The names below were confirmed in third-party full category lists (https://daltonluka.com/blog/google-my-business-categories and https://tradeloper.com/resources/google-business-profile-categories, both V); confirm each in the picker.

| Slot | Category | Verdict |
|---|---|---|
| Primary | **Swimming pool contractor** | Use. Third-party guide: "Building and installing pools, not cleaning them." This is the money category. |
| Additional 1 | **Landscaper** | Use. Covers design-build landscape work. |
| Additional 2 | **Landscape designer** | Use. Matches the design-led offer. Avoid "Landscape architect" (licensed title in most states). |
| Additional 3 | **Swimming pool repair service** | Use only if you take repair or resurface work, not only builds. |
| Additional 4 | **Pool cleaning service** | Only if you sell maintenance to the public. It pulls weekly-route searches you may not want. |
| Test later | **Fountain contractor**, **Landscape lighting designer**, **Basketball court contractor** (sport courts), **Paving contractor** (hardscape), **Lawn sprinkler system contractor** | Add one at a time, only for work you really do and want leads for. |
| Skip | Home automation company, Masonry contractor, General contractor | Dilutes the primary. |

Third-party tools report a cap of 1 primary plus 9 additional. Google's own page does not state a number, so treat the cap as unverified and stay at 4 or 5 total.

### 1.3 Business info fields
- **Name:** exactly "Arise Pools & Landscaping."
- **Description (max 750 characters, no URLs, per https://support.google.com/business/answer/3039617).** Draft (about 650 characters, edit freely):
  > Arise Pools & Landscaping is a licensed design-build company in Gilbert, Arizona. We design and build custom pools, pool remodels, landscapes, outdoor kitchens, hardscape, sport courts, and water and fire features for homeowners across the Phoenix East Valley, including Gilbert, Chandler, Mesa, Scottsdale, Queen Creek, and San Tan Valley. One team handles design, permits, construction, and Pentair pool automation, and we offer pool and landscape maintenance after the build. We hold Arizona ROC licenses 342276 (commercial) and 342277 (residential). Book a design call to talk through your lot, your HOA requirements, and your budget.
- **Opening date:** Google can show years in business. Use the true company date (BBB says 8/23/2022; confirm). Do not write "15 years" in the description unless it is true of the company.
- **Website link:** `https://www.arisepal.com/` (optionally add `?utm_source=google&utm_medium=organic&utm_campaign=gbp` to separate GBP traffic in GA4). **Appointment link:** `https://www.arisepal.com/book`.
- **Phone:** (480) 234-8900 as primary.
- **Hours:** Google says businesses that operate only by appointment should not list hours. Settle audit item M8 first, then mirror the website.
- **Service areas (max 20, by city or ZIP, not radius; should stay within about 2 hours' drive):** Gilbert, Chandler, Mesa, Scottsdale, Queen Creek, San Tan Valley, Phoenix, Tempe, Paradise Valley, Fountain Hills, Cave Creek. Optional if you really go there: Gold Canyon (two portfolio projects), Apache Junction, Carefree.

### 1.4 Services list
Use the services editor (https://support.google.com/business/answer/9455399): no prices, phone numbers or profanity in custom service names, and add a one or two sentence description to each. Map to the site's pages:

| GBP service | Site page |
|---|---|
| Custom pool design and construction | /services/custom-pools |
| Pool remodel and renovation | /services/pool-remodels |
| Landscape design and installation | /services/landscape-design |
| Outdoor kitchens and outdoor living | /services/outdoor-living |
| Hardscape, pavers and patios | /services/hardscape |
| Sport courts and pickleball courts (only if offered) | /services/hardscape |
| Water features and fire features | /services/water-fire-features |
| Pool automation (Pentair) | /services/smart-pool |
| Pool and landscape maintenance | /services/pool-maintenance |

### 1.5 Photos and video
- Specs from Google (https://support.google.com/business/answer/6103862): JPG or PNG, 10 KB to 5 MB, recommended 720 by 720, minimum 250 by 250, in focus, "no significant alterations or excessive use of filters." Video: up to 30 seconds, up to 75 MB, 720p or higher.
- Set a logo and a cover photo. Upload by category: finished pools (day and dusk), construction in progress, crew at work, outdoor kitchens, fire and water features, before and afters.
- **Cadence (my recommendation, not a Google rule):** 30 to 40 photos at launch from the five live portfolio projects, then 2 to 3 per week or about 10 per month, plus one 15 to 30 second drone clip per month. Name files descriptively before upload.
- Only upload photos you own the rights to. Remove client faces or house numbers if the client has not agreed.

### 1.6 Posts
Post types are Update, Offer, Event, with scheduling and recurring options (https://support.google.com/business/answer/7342169). Post weekly. Rotation: project spotlight (link to /portfolio), monsoon prep or recovery tip (link to the checklist), seasonal reminder (pre-summer, October swim season), permit or HOA tip, behind-the-scenes build photo, maintenance tip. Keep promotions out of the profile description.

### 1.7 Products, attributes, extras
Not a retail business, so skip Products. Fill every attribute Google offers for the category. Turn on messaging only if someone replies within the hour.

### 1.8 Q&A (changed, plan around it)
Google discontinued the Q&A API on November 3, 2025 (https://developers.google.com/my-business/content/qanda/change-log, V) and public Q&A is being replaced by an AI "Ask Maps" feature that answers from your profile data, reviews and photos (BrightLocal: https://www.brightlocal.com/learn/google-q-and-a/ and Footbridge: https://www.footbridgemedia.com/marketing-tips/google-shutting-down-gbp-q-a, both V; those are marketing sources, not a Google announcement). Practical effect: you cannot seed questions. Instead make the profile and site answer the questions: full services list, descriptions, service areas, permit and HOA FAQs on the site, and reviews that name the work.

### 1.9 Review request flow (compliant)
1. Generate the link or QR code on a computer: Business Profile, Read reviews, Get more reviews (https://support.google.com/business/answer/16816815).
2. Trigger points: at the final walkthrough, again 7 days after turnover, and once to every past client.
3. Same message to **every** customer by text and email. No pre-screening, no "how did we do?" survey that routes happy people to Google and unhappy people elsewhere (that is review gating).
4. Template: "Hi [Name], thank you for trusting Arise with your backyard. If you have a minute, an honest review on Google helps neighbors find us: [link]. Whatever you share, good or critical, we read all of it."
5. No incentives of any kind, no asking for specific wording, no staff quotas or commissions tied to review counts. All three are listed as prohibited behaviors on Google's policy page (https://support.google.com/contributionpolicy/answer/7400114).
6. Reply to every review within two business days: short, specific, no promotions (https://support.google.com/business/answer/3474122). For a bad review: acknowledge, offer a phone call, do not argue, flag only genuine policy violations (https://support.google.com/business/answer/4596773).
7. **Yelp is different:** do not ask customers for Yelp reviews (Section 7).
8. Goal (estimate): 8 to 15 genuine Google reviews in 90 days if you ask all past clients plus new turnovers.

### 1.10 Optional paid layer: Local Services Ads
Google's pages list pool contracting and landscaping among eligible trades, but eligibility varies by market and requires screening and verification (search summary, confirm inside the account). Info: https://business.google.com/us/ad-solutions/local-service-ads/ (V). Sign-up link from Google's service-area help page: https://ads.google.com/localservices/signup/ (V). Decide after 90 days of organic work.

### 1.11 Site-side tie-ins (dev tasks, not owner hours)
Add the GBP link, BBB link and social links to the footer; add `sameAs`, `addressLocality` and `postalCode` to the JSON-LD (audit M9); redirect the apex domain to `www` (audit H4) so citations and links consolidate on one hostname.

---

## 2. Core citations (NAP consistency): 33 targets

Rules: copy the canonical NAP exactly; same primary category wording; same URL with `www`; same hours; never type a tracking phone number unless it is also the site's number. Keep a tracking sheet: directory, URL of the live listing, date, login owner, NAP matches (yes or no).

Priority key: **P0** weeks 1 to 3, **P1** weeks 3 to 5, **P2** weeks 5 to 9, **P3** optional.

| # | Directory | Listing or claim URL | Cost | Priority | Check | Notes |
|---|---|---|---|---|---|---|
| C1 | Google Business Profile | https://business.google.com/us/business-profile/ | Free | P0 | V | Section 1. |
| C2 | Apple Business Connect | https://businessconnect.apple.com/ (redirects to https://business.apple.com/); help: https://support.apple.com/business | Free | P0 | V | Needs an Apple Account with a phone number. Service-area businesses sometimes cannot claim an existing place card; if you hit "cannot be claimed," use the business-without-a-public-location path or contact Apple support (search summary, U). |
| C3 | Bing Places | https://www.bingplaces.com/ (redirects to https://www.bing.com/forbusiness/) | Free | P0 | V | Can import from GBP; do it after GBP is verified. |
| C4 | BBB (existing profile) | https://www.bbb.org/get-listed to search or claim; profile above; accreditation info https://www.bbb.org/get-accredited and https://www.bbb.org/apply | Listing free; accreditation is paid and priced by the local BBB | P0 | V | Fix NAP on the existing profile. Use the BBB seal only as BBB's rules allow. |
| C5 | Facebook Business Page | Existing page linked from BBB: https://www.facebook.com/profile.php?id=100087511008198 | Free | P0 | S | Confirm you control it; set name, phone, address or service area, website, hours to the canonical record. |
| C6 | Yelp for Business | https://biz.yelp.com/claim | Free to claim; Yelp Ads are paid | P1 | V | Claim and complete. **Never ask customers for Yelp reviews.** |
| C7 | Nextdoor Business Page | https://business.nextdoor.com/en-us/getting-started/business-page | Free to claim (commonly reported; the page itself does not state a price); ads paid | P1 | V | Strong for neighborhood-level recommendations in Gilbert, Queen Creek, San Tan Valley. Ask real neighbors to recommend you; no incentives. |
| C8 | Houzz (free basic profile) | https://www.houzz.com/pro/join (also https://pro.houzz.com/pro). How-to: https://pro.houzz.com/pro-help/r/how-to-create-a-business-profile-on-houzz | Free basic; paid tiers and ads exist | P1 | V | Pick the swimming pool builder and landscape categories; add address or service area and website or the profile will not list in the directory (Houzz guidance). Upload the five live projects with captions and city names. |
| C9 | BuildZoom | https://www.buildzoom.com/ | Free to claim per a third-party guide; 2.5% referral fee and $99/month upgrade also reported (U) | P2 | V | License-based profile; Arizona profiles point to the ROC for status. Read the contractor sign-up terms before claiming. |
| C10 | Angi (HomeAdvisor merged into Angi) | https://signup.angi.com/pro | Pay per lead and/or membership; third-party estimates $15 to $85 per lead (U) | P3 | V | Shared leads, lead quality complaints, FTC settlement history with HomeAdvisor (search summary). Skip unless you want a paid lead channel. |
| C11 | Thumbtack | https://www.thumbtack.com/pro | Free profile, pay per lead (the page says "no charge to join" but lead budgets drive volume) | P3 | V | Optional paid channel. |
| C12 | Porch | https://pro.porch.com/pro | Not verified | P3 | V | Page loads; pricing and fit for pool builders not verified. |
| C13 | Data Axle (data aggregator) | https://www.data-axle.com/marketing-solutions/local-listings-management/ | Free per Data Axle | P2 | V | Feeds many partner sites. Search for the business, correct it, verify. **Not** expressupdateusa.com (hijacked). |
| C14 | Foursquare | https://foursquare.com/add-place (login) and https://location.foursquare.com/ | Free | P2 | V | Feeds several apps. |
| C15 | Yellow Pages (YP) | https://www.yellowpages.com/ | Free basic | P3 | S | Site blocks automated checks; the claim flow is unverified. Often populated by aggregators; check after C13. |
| C16 | MapQuest | https://www.mapquest.com/ | Free | P3 | V | Claim route unverified; usually fed by aggregators. |
| C17 | Alignable | https://www.alignable.com/ | Free | P3 | V | Local small-business network; useful for referrals, weak for links. |
| C18 | LinkedIn Company Page | https://www.linkedin.com/company/setup/new/ | Free | P2 | V (login redirect) | Add to `sameAs`. |
| C19 | Instagram business profile | https://www.instagram.com/accounts/emailsignup/ | Free | P2 | V | Add to `sameAs`. Link bio to the portfolio. |
| C20 | Pinterest Business | https://business.pinterest.com/ | Free | P2 | V | Pool and landscape imagery performs here; claim the website. |
| C21 | YouTube channel | https://www.youtube.com/create_channel | Free | P2 | V | Drone walk-throughs of the five live projects; description links to the matching /portfolio and city pages. |
| C22 | Arizona ROC contractor record | https://azroc.my.site.com/AZRoc/s/contractor-search (agency site: https://roc.az.gov/) | Free | P0 | V (search tool), S (agency site) | Not a link source. Verify business name, phone, address and classifications for 342276 and 342277 match the canonical NAP; request corrections with the ROC. |
| C23 | Arizona Corporation Commission business record | https://arizonabusinesscenter.azcc.gov/ | Free to view | P0 | V | Confirm the legal entity name and statutory agent match what BBB and the site say. |
| C24 | Gilbert Chamber of Commerce | Join: https://gilbertaz.com/join-today ; directory: https://business.gilbertaz.com/list/ | Paid, dues not published | P1 | V | Home-city chamber (gilbertchamber.com now redirects to gilbertaz.com). Ask whether the directory listing gets a followed website link. |
| C25 | Chandler Chamber | Join: https://business.chandlerchamber.com/member/newmemberapp ; directory: https://business.chandlerchamber.com/list/ | Paid, dues not published | P2 | V | |
| C26 | Mesa Chamber | Join: https://business.mesachamber.org/member-application ; directory: https://business.mesachamber.org/list ; phone (480) 969-1307 per the site | Paid, dues not published | P2 | V | |
| C27 | Scottsdale Chamber | Join: https://business.scottsdalechamber.com/member/newmemberapp ; directory: https://business.scottsdalechamber.com/list | Paid, dues not published | P2 | V | Scottsdale is a high-value city; no Scottsdale project exists in the portfolio yet (audit H1), so lead with permits and HOA expertise. |
| C28 | Queen Creek Chamber | Join: https://queencreekchamber.com/join-the-chamber/ ; directory: https://queencreekchamber.com/find-a-business/ | Paid, dues not published | P2 | V | Covers Queen Creek; San Tan Valley overlaps. |
| C29 | San Tan Valley Chamber | Membership interest form linked from https://santanvalleychamber.com/ | Paid, dues not published | P3 | V | Two portfolio projects and two blog posts target San Tan Valley. |
| C30 | Tempe Chamber | https://www.tempechamber.org/membership/ ; directory https://business.tempechamber.org/member-directory | Paid, dues not published | P3 | V | |
| C31 | Fountain Hills Chamber | Join: https://cm.fhchamber.com/member/newmemberapp/ ; directory: https://cm.fhchamber.com/list/ | Paid, dues not published | P3 | V | |
| C32 | Local First Arizona | https://localfirstaz.com/coalition-member (phone 602-956-0909) | $99 (1 to 4 employees), $199 (5 to 10), $299 (11 to 20), $399 (21 to 50), $499 (51+); 20% off for rural and nonprofits | P2 | V | Requires an Arizona-owned, independent business. Directories: https://explore.localfirstaz.com (V) and http://localistaz.com/ (V). Whether a member profile includes a website link is not stated. Do not claim membership on the site until accepted. |
| C33 | PHTA "Find a Pool Pro" directory | https://www.phta.org/consumer/directory/find-a-pool-pro/ | Included with or tied to PHTA membership (not stated on page) | P1 | V | See Section 3. |

Count: 33 listed (31 free or low-cost directories and chambers, plus the two record checks C22 and C23). Chambers have no published dues, so ask for the price and whether the directory link is followed before paying; limit yourself to two chambers in the first 90 days (Gilbert plus the one nearest your pipeline).

Other aggregator names appear in many citation guides (Neustar Localeze, Manta, Superpages). Their sites did not load for automated checks in this session, so they are **unverified** and left out. Add them only after a citation audit shows a mismatch they caused.

---

## 3. Industry and supplier backlinks

### 3.1 Pool industry

| Program | What you get | How to qualify | Cost | URL | Check |
|---|---|---|---|---|---|
| **PHTA (Pool & Hot Tub Alliance), Builder/Installer membership** | National trade association (about 4,000 members per its home page). Benefits listed: up to $500 off GENESIS and PHTA courses, research reports, job board, one free PHTA/ANSI standard per year, one free entry to the International Awards of Excellence. | Company membership for firms that build, install and renovate pools, spas and water features. | By annual sales: under $1.5M $618/yr; $1.5M to $2.49M $773; $2.5M to $4.9M $1,030; $5M to $9.9M $2,060; $10M to $19.9M $3,090; $20M to $30M $4,120; $30M+ $5,150. Monthly payment option; no refunds. | Page: https://www.phta.org/membership/join-phta/phta-builder-installer-membership/ ; join: https://portal.phta.org/Membership/Join/Builder-Installer/B-Company ; help 703-838-0083 ext. 116, membership@phta.org | V |
| **PHTA "Find a Pool Pro" directory** | Consumer directory (3,202 results when loaded) listing builders with specialties and any certifications (for example CBP). | The page does not say how listing works. Ask PHTA membership whether Builder/Installer members are listed and how to add specialties. | Not stated | https://www.phta.org/consumer/directory/find-a-pool-pro/ ; landing page https://www.phta.org/consumer/find-a-pro/ | V |
| **PHTA Awards of Excellence** | Industry awards for installed projects, usable in press and on the site. | PHTA members only; more than 20 categories; entry timing for the next cycle not confirmed. | One free entry with Builder/Installer membership | https://www.phta.org/membership/promote-your-business/phta-awards-of-excellence/international-awards-of-excellence | V |
| **PHTA Central Arizona Chapter** | Local networking with the Phoenix pool trade; chapter page. | Contact PHTA Chapter Services (membership@phta.org) for how to join. | Not stated | PHTA chapter list: https://www.phta.org/membership/chapters/phta-chapters/ ; chapter Facebook page: https://www.facebook.com/PHTA-Central-Arizona-Chapter-formerly-APSP-234734016547706 | V (chapter list), S (Facebook). The chapter's own member directory URL (phtacentralaz.org/member-directory) appeared in search but returned 404 in this session. |
| **Pool & Spa News Top 50 Builders** | National ranking; winners featured in the June issue; strong editorial backlink and PR value. | 2025 residential construction revenue of $2.5 million or more; scored on revenue, staff training, industry involvement, web presence and community involvement. The 2026 cycle's final deadline was March 20, 2026; expect a similar early-2027 window (U). | Entry fee not stated | https://psntop50builders.secure-platform.com/ ; 2025 winners page https://www.poolspanews.com/companies/top-50-builders/meet-the-2025-psn-hayward-top-50-builders_o/ | V |
| **PoolContractor.com** ("largest directory of pool contractors") | Directory listing. | "Get Listed Today" form. | Not stated; the forms showed a security-check error when loaded; operator not named. Verify before paying. | https://www.poolcontractor.com/join | V (page), U (terms) |
| **IPSSA Region 8 (service techs), East Valley chapter** | Maintenance-side networking; East Valley chapter meets third Thursday at 6 pm at Pool & Electrical Products, 2900 S Gilbert Rd, Chandler. | Open to pool service pros. Relevant only to the maintenance line. | Not stated | https://ipssa.com/Web/Web/Regional-Board-of-Directors-List/Region-8.aspx | V |
| **Desert Pool & Spa Show** | Trade show for the Arizona pool trade, listed for January 9, 2027 in Phoenix (venue not confirmed). | Trade-oriented, run by IPSSA Region 8. Supplier networking, not consumer leads. | Not stated | https://poolcompanysoftware.poolbrain.com/pool-brain-blog/pool-spa-industry-conferences-2026-2027 | V (calendar), U (dates) |

Invitation-only groups (long-term, not a 90-day task): Master Pools Guild (invitation only, 5 years in business, gunite or shotcrete focus; secondhand sources) and Genesis 3 Design Group (education-based membership; application terms not found). Both are unverified; do not promise either on the site.

### 3.2 Manufacturer and supplier programs (only real, verified ones)

Rule: link only to programs where Arise actually installs the product. The site currently names only Pentair.

| Program | What it is | Reality check | URL | Check |
|---|---|---|---|---|
| **Pentair Pool app "Pro Locator" and Pentair Partner programs** | Pentair's FAQ says homeowners can find local providers enrolled in a Pentair Partner program, and that remote-monitoring benefits require enrollment. | Eligibility for pool builders is **not** stated. Ask your Pentair rep or distributor to enroll Arise and to confirm Pro Locator listing. | FAQ: https://www.pentair.com/app-support/app-faqs.html ; partner portal: https://partners.pentair.com/ | V |
| **Pentair "Find a Dealer" locator (pool and spa)** | Public dealer locator. | The page gives no listing process and carries a disclaimer that it is not an endorsement. Ask the distributor how dealers are added. | https://www.pentair.com/en-us/find-a-dealer/pool-spa.html | V |
| **Pentair True Blue PRO Dealer Network** | A real program, but for water treatment dealers and requires a Google rating of 4.0 or higher. | **Not relevant** to pool building. Skip. | (terms PDF returned by search) | U |
| **PebbleTec "Find a PebbleTec Builder"** | Builder locator with Elite Builders, Certified Builders and Authorized Installers; 21-step onboarding. | Only if Arise uses PebbleTec finishes. Apply through PebbleTec. | https://pebbletec.com/find-a-builder/ | V |
| **Belgard Authorized Contractor locator** | ICPI-trained paver contractor network. | Only if Arise installs Belgard. The page blocked automated checks; URL taken from a search summary. | https://www.belgard.com/Locator | S, U |
| **Jandy (Fluidra) dealer locator** | "Find a Dealer" page. | Dealer locator, not a builder program. Only if you install Jandy. | https://www.jandy.com/locator | V |
| **Hayward** | I found no builder locator. | Unverified. Ask the distributor. | none | U |

Local supply houses: the IPSSA page names Pool & Electrical Products (Chandler), SCP (Phoenix) and Superior Pool Products (Mesa) as chapter hosts. Ask each for a "builder partners" or "preferred contractor" page and a link; their sites were not checked.

### 3.3 Landscape and trade associations

| Association | Value | Qualify | Cost | URL | Check |
|---|---|---|---|---|---|
| **Arizona Landscape Contractors' Association (ALCA)** | Member directory, annual trade show, Excellence in Landscaping Awards, ACLP and irrigation certifications, monthly member mixers, sponsorship program. | Open to licensed contractors; the page states no license requirement. Confirm your ROC classifications fit a landscape contractor. | Contractors by annual sales: under $100k $300; $100,001 to $500k $420; to $1.5M $650; over $1.5M $980. Associates $600 to $1,200. Architects & Designers $300. HOAs and municipalities $175. | https://alca.org/membership/ ; apply (linked from that page): https://alca.site-ym.com/general/register_member_type.asp ; sponsors: https://alca.org/sponsors/ | V (alca.org), S (application and directory hosts) |
| **Arizona Nursery Association (AZNA)** | Nursery and landscape supply chain; supports the Smartscape program. | Membership terms not verified. | U | https://www.azna.org/ | V (home page only) |
| **National Association of Landscape Professionals (NALP)** | National directory ("Find a Member") and join page. | Join link on home page; dues not verified. | U | https://www.landscapeprofessionals.org/ | V (home page only) |
| **AMWUA Smartscape program** | Water-wise training for landscape and irrigation pros (AMWUA, Tucson Water, UA Cooperative Extension, ADWR, with ALCA and AZNA support). Ask whether trained firms are listed. | Staff complete the training. | U | https://www.amwua.org/plants/tools ; campaign site https://wateruseitwisely.com/ | V |
| **Home Builders Association of Central Arizona (HBACA)** | Residential construction trade group (since 1951). | Affiliate or remodeler membership terms not verified. I found no East Valley Parade of Homes with an exhibitor sign-up (the Parade of Homes I found is Tucson's). | U | https://www.hbaca.org/ | V (home page only) |

### 3.4 HOA and community-association channel
- **CAI Arizona chapter**, Business Partner category: https://www.cai-az.org/CAIAZ-Business-Partners (V). Online provider directory: https://www.cai-az.org/onlinedirectory (V). Annual sponsorship: https://www.cai-az.org/annualsponsorship (V). Events: https://www.cai-az.org/eventcalendar (U). Join link on that page: https://www.caionline.org/become-a-member/ (S). Dues are not listed.
- **AACM (Arizona Association of Community Managers):** https://www.aacm.com/ (V). Its affiliate program covers suppliers to HOA communities and management companies (search summary); a public vendor directory is unverified.
- Why it matters: your blog already has HOA-focused posts (Power Ranch, Johnson Ranch, Scottsdale permits). Management companies keep preferred vendor lists and write the newsletters.

---

## 4. Local and editorial opportunities

### 4.1 Publications, awards and tours

| Outlet or program | What to pitch or enter | Contact or submission page | Check |
|---|---|---|---|
| **Phoenix Home & Garden, Readers' Choice 2027** | Nominations Oct 1 to 25, finalist voting Nov 1 to 30, winners in the Feb/March 2027 issue. Local Arizona businesses only; most nominations advance to the finals. Categories are not shown on the page, so check the ballot for pool, landscape and home categories. Do not offer incentives for nominations or votes. | https://www.phgmag.com/2027-readers-choice-ballot/ ; questions matthew.johnson@citieswestmedia.com ; ballot ads marketing@citieswestmedia.com (both from that page) | V |
| **Phoenix Home & Garden, PH&G Honors** | Design awards since 1980. Categories include **Pool Design** and **Residential Landscape**. 2026 entries are closed; for 2026 projects had to be completed March 2024 to March 2026 (next window unverified). Fees: $200 first entry, $175 each additional. Needs 300-word descriptions and 1 to 7 professionally shot photos (JPEG or TIFF, 300 dpi, at least 2,000 px wide); renderings not allowed. Winners get a trophy and marketing toolkit. Independent national judges. | https://www.phgmag.com/phg-honors/ ; phg-honors@phgmag.com | V |
| **Phoenix Home & Garden, home and garden tours** | Tours feature designers and builders; submission or sponsorship process is not stated on the page. Ask the magazine. | https://www.phgmag.com/home-garden-tours/ ; contact https://www.phgmag.com/contact/ ; advertising@phgmag.com ; office 480-664-3960, 6310 E Thomas Rd #200, Scottsdale AZ 85251 | V |
| **Phoenix Magazine** (Best of the Valley reader poll, editorial) | Pitch the monsoon checklist or a design story. The Best of the Valley categories were not confirmed. | Editorial: https://www.phoenixmag.com/editorial-contact/ ; advertising: https://www.phoenixmag.com/advertising/ ; poll link http://phoenixmag.com/votebov | V (editorial), S (advertising and poll returned 502 on automation) |
| **AZ Big Media / Ranking Arizona** | Business-press features, sponsored content, and a reader-vote ranking whose listed contact is a sales director. The audit flagged a "Ranking Arizona" claim on press.html. Treat ranking programs as advertising unless proven otherwise. | General info@azbigmedia.com ; form https://azbigmedia.com/contact/ ; sponsored content https://azbigmedia.com/category/sponsored-content/ ; Ranking Arizona https://azbigmedia.com/vote-ranking-arizona/ ; editorial and sales contacts are listed on the contact page | V |
| **Gilbert Sun News (Times Media Group)** | Local-business and homeowner stories (permits, HOA, monsoon). | Contact https://www.gilbertsunnews.com/site/contact.html ; editor@gilbertsunnews.com ; advertising https://www.timeslocalmedia.com/advertise/ ; 1900 W. Broadway Road, Tempe, 480-898-6500 (all from the page). No news-release form was found. | V |
| **Gilbert Independent** | Same pitch angles. | https://www.gilbertindependent.com/ (page text did not load fully; contact route unverified) | V (home), U (contact) |
| **East Valley Tribune** | Same. | https://www.eastvalleytribune.com/ (home page only; contact route unverified) | V, U |
| **Fountain Hills Times** | Fountain Hills projects and guides. | https://www.fountainhillstimes.com/ (home page only) | V, U |
| **Free journalist-query platforms** | Answer reporter requests about pool costs, monsoon damage and water use with specific, honest expertise. | Qwoted https://www.qwoted.com/ (free tier limits pitches); Featured https://featured.com/ ; Source of Sources https://www.sourceofsources.com/ (free) | V (all three load); pricing is from third-party reviews, so confirm |

### 4.2 Home shows and tours
- **Maricopa County Home & Garden Show:** January 15 to 17, 2027, Arizona State Fairgrounds, organizer says it has run since 1992 and welcomes landscaping and outdoor living businesses (search summaries put attendance near 50,000). Vendor application: https://maricopacountyhomeshows.com/become-a-vendor/ ; contact form https://maricopacountyhomeshows.com/contact/ (V). Local First Arizona also lists the vendor opportunity: https://localfirstaz.com/upcoming-vendor-opportunities/mchsjan2027 (V). A phone number (602-485-1691) and a booth price range appeared only in a search summary: unverified.
- **Phoenix-area "Parade of Homes" or backyard tour:** I found none with an exhibitor sign-up in the East Valley. The Parade of Homes I found belongs to the Southern Arizona Home Builders Association in Tucson. Ask HBACA (https://www.hbaca.org/) and PH&G whether a backyard or outdoor-living tour accepts builders.
- **PH&G tours** (above) are the closest editorial equivalent.

### 4.3 Realtor and HOA partnerships
- **WeSERV (West and South East Realtors of the Valley)**, the merged successor of SEVRAR per its own site; Southeast Valley chapter office in Chandler, main office 480-477-5882. Become a member: https://weserv.realtor/become-a-member/ (V). Affiliate directory: https://members.weserv.realtor/affiliate-member-directory (V) (categories shown include HVAC and roofing; pool and landscape categories did not appear, so ask). Contact: https://members.weserv.realtor/contact (V). Affiliate terms and dues: unverified.
- **Phoenix REALTORS:** https://www.phoenixrealtors.com/ (V), office 602.246.1012; a vendor affiliate program is not described on the affiliates page (V). Ask by phone.
- **Offer to realtors:** a one-page "Pool and backyard buyer's guide" (inspection items, permit history, HOA rules) and a lunch-and-learn. Keep claims factual.
- **HOA newsletters:** Power Ranch Community Association, site https://mypowerranch.com/ (V), listed as managed by CCMC (AZ HOA Watch: https://azhoawatch.org/power-ranch-community-association/ , V). Ask the manager about newsletter articles, sponsor slots and the approved-vendor process. Do the same for Johnson Ranch (San Tan Valley) and other communities named in your blog posts. Newsletter ad programs are unverified.

### 4.4 Local sponsorships (pick one or two, not all)
- Chamber sponsorship pages: Gilbert https://gilbertaz.com/sponsorship-opportunities ; Chandler https://www.chandlerchamber.com/sponsorships/ ; Mesa https://www.mesachamber.org/ad-catalog/ ; Scottsdale https://www.scottsdalechamber.com/exposure/ ; Queen Creek https://queencreekchamber.com/sponsorships/ (all V).
- Local First Arizona's fall festival sponsor packet: https://localfirstaz.com/s/AZ-Fall-Festival-Sponsor-Opps-2026.pdf (V). Signature events: https://localfirstaz.com/signature-events (V).
- Service club: Gilbert Rotary, https://www.gilbertrotary.org/ (V). Sponsorship terms unverified.
- **Water-safety partnership (fits a pool builder naturally):** Phoenix Children's water safety program https://www.phoenixchildrens.org/water-safety (V; redirects to the program page), CDC Foundation Arizona Drowning Data Report https://www.cdcfoundation.org/Arizona-Drowning-Data-Report (V), and the ASU, Michael Phelps Foundation and Phoenix Children's program https://news.asu.edu/20210527-arizona-state-university-launches-water-safety-education-program-partnership-michael-phelps (V). A real offer (donated safety-barrier consultations, or a sponsored water-watcher event) can earn a legitimate mention. Never pay for the link itself.
- Sponsorship links are advertising. If a sponsor page gives you a link, ask for `rel="sponsored"` or accept that it carries no ranking value; the value is local visibility and referrals.

---

## 5. Content-led link ideas tied to existing assets

Existing assets (from the repo): blog posts at /blog (12), city pages at /cities/* (11), /portfolio (5 live projects in `data/projects.json`: The Desert Escape, Legacy Living, The Hidden Jewel, The Modern Escape, Family Focused), /guide, /reviews. The audit says city pages are thin (M5), so upgrade the asset first, then pitch.

| # | Asset to build or upgrade | Hook | Who might link | Outreach target |
|---|---|---|---|---|
| 1 | **Monsoon pool recovery checklist** (exists: /blog/monsoon-pool-recovery-checklist, about 990 words). Add a one-page printable PDF, an annotated photo, and a storm-damage "when to call a pro" box. | Seasonal (June to September) and useful to every pool owner and property manager. | HOA newsletters, property managers, realtors, local news weather segments, Nextdoor | CAI Arizona / AACM contacts, Gilbert Sun News, WeSERV agents, Nextdoor posts |
| 2 | **Permits and HOA approval guides by city** (exists for Scottsdale: /blog/pool-permits-and-hoa-approval-in-scottsdale). Clone the format for Gilbert, Chandler, Queen Creek, Mesa and Paradise Valley. | Cite the Arizona pool barrier statute (https://www.azleg.gov/ars/36/01681.htm, V) and each city's current requirements. I could not find a current official Gilbert pool-barrier page (a 2003 policy PDF appeared), so confirm requirements with Gilbert Development Services before publishing. | City-resource pages, HOA managers, realtors, neighborhood sites | Each city's chamber relocation page; HOA managers; WeSERV |
| 3 | **Gilbert grass-removal rebate guide** (new, under /cities/gilbert and landscape design). What qualifies, what to plant, a before and after, a cost range. | Per news coverage, Gilbert offers up to $800 for residential grass removal and up to $3,000 for businesses and HOAs, with a smart-controller rebate of up to $250 (confirm current terms at gilbertaz.gov before publishing). Sources: https://www.azfamily.com/2026/05/13/gilbert-seeks-federal-grant-expand-grass-removal-rebate-program/ (V) and https://ktar.com/arizona-news/gilbert-grass-removal-rebate-low-water-landscape-yards (S). | Water-conservation pages, HOA boards, local news, AMWUA/Water Use It Wisely readers | Gilbert Sun News, HOA managers, https://wateruseitwisely.com/conserve-with-us/ (V; the home page does not say who it is for) |
| 4 | **Original data post: "What East Valley pools cost in 2026."** Expand /blog/what-a-125k-pool-actually-gets-you-2026 with Arise's own anonymized project ranges by city and feature. Publish only real numbers. | Local reporters and personal-finance writers cite real local cost data. | AZ Big Media, Phoenix Magazine editors, realtors, lenders | Section 4.1 contacts; Qwoted and Featured queries on pool costs |
| 5 | **City guides upgraded to 300+ words** with named neighborhoods, HOA norms, one real portfolio project each. Start with Gilbert, San Tan Valley, Queen Creek, Chandler. | Neighborhood and relocation pages link to useful local guides. | Chambers, neighborhood associations, realtors | Chamber member pages (Section 2) |
| 6 | **Portfolio as an award and editorial feed.** Hire a photographer for the strongest 2 projects (PH&G Honors needs professionally shot, 2,000 px wide images). | Awards give you a citable, linkable credential. | PH&G, PHTA, ALCA Excellence in Landscaping, Pool & Spa News | Section 3 and 4 entries |
| 7 | **Hard water and scale guide** (exists: /blog/hard-water-and-calcium-scale-on-arizona-pools). Add a photo diagnostic table (scale vs efflorescence vs etching). | Pool service techs share diagnostic aids. | IPSSA East Valley chapter, pool supply stores, local pool-service blogs | IPSSA chapter meeting; supply-house counter staff |
| 8 | **Pickleball and sport court guide for HOAs** (the Legacy Living project includes a lit pickleball court). Cover noise, lighting, HOA approval and surface choices. | Pickleball demand is high; HOAs ask for guidance. | HOA managers, pickleball groups, local news | CAI Arizona / AACM |
| 9 | **Backyard water-safety page** (barriers, covers, alarms, supervision) co-authored with or reviewed by a water-safety partner. | Safety resource pages are linkable and mission-aligned. | Hospital and fire-department safety pages, schools, realtors | Phoenix Children's water-safety program, local fire departments (Section 4.4) |
| 10 | **Fix the /guide promise** (audit M2: "Send Me the Playbook" delivers nothing). Deliver a real PDF; it becomes the outreach attachment. | A real download is the cheapest linkable asset you already advertise. | All of the above | all |

Anchor text rule for any request: branded or plain URL anchors only, never exact-match "pool builder Gilbert" anchors on outreach.

---

## 6. 90-day execution schedule (week 1 starts Monday, October 19, 2026)

Owner time only; writing, design and site changes are separate tasks I can do. Total about 58 hours (about 53 if you skip the home-show booth).

| Wk | Dates | Owner tasks | Hrs |
|---|---|---|---|
| 1 | Oct 19 to 25 | Lock the canonical NAP and hours. Decide service-area vs hybrid. Search Google Maps for an existing listing. Confirm the BBB and Facebook records are yours; email or call the local BBB to correct address, phone, hours (BBB profile data in Section 0). Invite 5 to 10 happy past clients to nominate you in the PH&G Readers' Choice before Oct 25 (no incentive, no script). Collect 40 best project photos, logo, license proof. | 5 |
| 2 | Oct 26 to Nov 1 | Create or claim and verify the GBP. Set categories, 11 service areas, services list, description, opening date, 30 to 40 photos, first post. | 6 |
| 3 | Nov 2 to 8 | Apple Business Connect, Bing Places (import from GBP), reclaim the Facebook page, Yelp claim (no review requests), Nextdoor Business Page. | 5 |
| 4 | Nov 9 to 15 | Houzz free profile with the five live projects, BuildZoom claim, LinkedIn, Pinterest, YouTube (one drone clip). Verify the ROC and Corporation Commission records match. Approve site footer and `sameAs` changes. | 5 |
| 5 | Nov 16 to 22 | Data Axle check, Foursquare. Sweep for duplicates. Turn on the review system (Google link and QR, text and email template, who sends it). One-time ask to all past clients. Start weekly GBP posts and review replies. | 4 |
| 6 | Nov 23 to 29 | Thanksgiving week, light: posts and review replies. Call PHTA membership (703-838-0083 ext. 116) and ask about Find a Pro listing and Builder/Installer dues for your sales tier. | 2 |
| 7 | Nov 30 to Dec 6 | Join PHTA if approved ($618 to $1,030 for the three lowest tiers). Call your Pentair rep or distributor about Partners enrollment and Pro Locator. Email the PHTA Central Arizona chapter. Call Gilbert Chamber for dues and directory link rules. ALCA join decision. | 5 |
| 8 | Dec 7 to 13 | Join Gilbert Chamber if the numbers work. Inquire with CAI Arizona (Business Partner), AACM and WeSERV affiliates. Review and approve the monsoon checklist PDF and the Gilbert permits and HOA guide. | 5 |
| 9 | Dec 14 to 20 | Outreach batch 1 (10 targets): HOA managers, 3 realtors, 2 local reporters, using the checklist PDF and permit guide. Set up Qwoted, Featured and Source of Sources accounts (free tiers) and answer 3 queries. | 4 |
| 10 | Dec 21 to 27 | Holiday, light: posts and review replies. Book a photographer for the PH&G Honors-grade shoot. | 2 |
| 11 | Dec 28 to Jan 3 | Approve the Gilbert grass-removal guide and the cost data post (real numbers only). Apply to the Maricopa County Home & Garden Show or decide not to. | 3 |
| 12 | Jan 4 to 10 | Outreach batch 2: data post and rebate guide to AZ Big Media, Gilbert Sun News, Phoenix Magazine, East Valley Tribune. Pick one local sponsorship. Check Pool & Spa News Top 50 eligibility (revenue threshold $2.5M). | 4 |
| 13 | Jan 11 to 17 | Home show Jan 15 to 17 if you exhibit (8 hours total), or 3 hours to review. Run the 90-day scorecard (below). | 8 |

**Scorecard to run in week 13:** GBP views, calls, direction requests and website clicks (GBP Performance); count of genuine Google reviews and average rating; citation sheet match rate (target 100% NAP matches); referring domains from Google Search Console's Links report; leads from GBP, Houzz and referrals logged in GHL with source.

**Dependencies on site work (so links do not leak):** apex redirect to `www` (audit H4); remove or substantiate trust claims (H1); replace placeholder policy pages (H2); add `sameAs` and footer profile links (M9).

---

## 7. What NOT to do

1. **Do not buy links, sell links or join link schemes.** Google's spam policies list buying or selling links to manipulate ranking, excessive link exchanges, automated link creation and advertorials that pass ranking credit as link spam. Sponsored placements must be disclosed and not pass ranking credit (use `rel="sponsored"`). https://developers.google.com/search/docs/essentials/spam-policies (V).
2. **No PBNs, expired-domain blogs, or "guaranteed 50 backlinks" packages.** Private blog networks exist only to pass links and fall under the same policy. The search tool I used did not return Google wording that names PBNs, so this is an inference from the general definition (U).
3. **No review gating.** Do not screen customers with a survey and send only happy ones to Google. Google's policy bars selectively soliciting positive reviews and discouraging negative ones.
4. **No incentives for reviews** (discounts, gift cards, referral credit, "$500 credit" style offers tied to reviews), no paying for reviews, no asking for specific wording, no staff quotas for reviews. Google review policy: https://support.google.com/contributionpolicy/answer/7400114 (V). GBP representation rules: https://support.google.com/business/answer/3038177 (V). Restrictions for violations: https://support.google.com/business/answer/14114287 (V).
5. **Do not ask for reviews on Yelp.** Yelp's stated policy discourages solicitation and its software can hide solicited reviews (secondary source: https://www.brightlocal.com/learn/review-management/dos-and-donts/review-platform-guidelines/ , V; confirm in Yelp's own content guidelines).
6. **No fake or invented testimonials, awards, press or review counts.** The FTC's Trade Regulation Rule on consumer reviews and testimonials (16 CFR Part 465) bans fake reviews, buying reviews, undisclosed insider reviews, certain review suppression and conditioning incentives on sentiment. https://www.law.cornell.edu/cfr/text/16/part-465 (V) and https://www.federalregister.gov/documents/2024/08/22/2024-18519/trade-regulation-rule-on-the-use-of-consumer-reviews-and-testimonials (V). This applies directly to the unsubstantiated testimonials flagged in audit H1.
7. **No keyword-stuffed GBP name, fake address, mailbox or virtual office, and no second profile for the same business.** Do not list service areas you will not serve. All in https://support.google.com/business/answer/3038177 (V).
8. **No mass directory blasts or auto-submit tools** that create hundreds of low-quality listings with inconsistent NAP.
9. **No unattributed brand marks.** Use the BBB seal and any PHTA or manufacturer logos only when you hold the membership and follow their usage rules.
10. **Do not trust stale domains.** Check where a listing site redirects before entering business data (the expressupdateusa.com case).
11. **Do not over-optimize anchor text** or trade links reciprocally at scale.
12. **Ranking and "Best of" programs:** enter only if the rules allow it, never vote-stuff, and disclose paid placements.

Policy links in one place: Google Business Profile guidelines https://support.google.com/business/answer/3038177 ; Maps contributed-content policy https://support.google.com/contributionpolicy/answer/7400114 ; Search spam policies https://developers.google.com/search/docs/essentials/spam-policies .

---

## Appendix A: Things I could not verify

- Whether the existing BBB profile and Facebook profile belong to this business, and whether a Google Business Profile already exists.
- Dues for all chambers, CAI Arizona, WeSERV affiliates, PHTA Central Arizona chapter, AZNA, NALP, HBACA.
- How PHTA's Find a Pro directory adds builders, and whether Pentair Partner or Pro Locator enrollment accepts pool builders.
- Next-cycle dates for PH&G Honors, PHTA Awards of Excellence and Pool & Spa News Top 50; Maricopa show booth pricing; PH&G Readers' Choice category list and self-nomination rules.
- Claim flows and terms for Yellow Pages, MapQuest, Porch, Angi and Thumbtack pricing for pool builders; Manta, Superpages and Neustar Localeze were not loadable and are excluded.
- Hayward builder locator; Belgard locator (page blocks automation); Master Pools Guild and Genesis 3 current rules.
- Official current Gilbert pool-barrier page (only a 2003 policy PDF surfaced) and current Gilbert rebate amounts.
- East Valley Partnership membership (evp.org is parked; evp-az.org returned HTTP 500).
- Contact routes for the Gilbert Independent, East Valley Tribune and Fountain Hills Times; HOA newsletter ad programs.
- Which of Arise's ROC classifications qualify for ALCA membership.
