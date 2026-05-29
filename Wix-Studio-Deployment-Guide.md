# Arise Pools — Wix Studio Deployment Guide
**Staging Site:** Arise Pools Landsc (Draft)  
**Date:** May 2026  
**Status:** Use this guide for all manual steps that cannot be done via API.

---

## What's Already Done (via API ✅)

These are live on your staging site — no action needed:

- **DreamSubmissions CMS collection** — all 23 fields from `ghl.jsw` are present
- **12 blog posts** — published and indexed (pool cost, design styles, maintenance, the Arise Method, financing, desert landscaping, remodel vs replace, smart pool tech, build timing, outdoor kitchens, plunge pools, community)
- **`GHL_WEBHOOK_URL` secret** — set in Wix Secrets Manager (ID: `11b4198e-5319-47f1-9e26-0150546f2622`)

---

## ⚡ UPDATED APPROACH — Router Method (Faster)

Instead of creating 47 pages manually, use the **Velo Router** approach:
- Paste 2 backend files
- Create 1 router page (instead of 47 individual pages)
- All 47 URL slugs are handled automatically

**Time estimate: 30–45 minutes total** (vs 2–3 hours for 47 individual pages)

---

## What You Still Need to Do in Wix Studio

Everything below requires the Wix Studio editor. With the router approach, you only need to do **3 steps** plus configure navigation.

---

## STEP 1 — Deploy the GHL Backend (ghl.jsw)

This is the most important technical step. It wires the Dream Center form to GoHighLevel.

### 1A. Open the Wix Velo Code Panel

1. Open your staging site in **Wix Studio** (studio.wix.com)
2. In the left sidebar, click the **`</>` (Dev Mode / Code)** icon
3. If Velo isn't enabled, click **"Enable Dev Mode"** — confirm when prompted
4. In the file tree on the left, you'll see a **Backend** folder

### 1B. Create the backend file

1. Right-click the **Backend** folder → **New .jsw File**
2. Name it exactly: `ghl` (Wix adds the `.jsw` extension automatically)
3. The file path should read: `backend/ghl.jsw`

### 1C. Paste the code

1. Open this file on your computer:  
   `/Users/jakemedford/Documents/Claude/Projects/Arise Pools/wix-velo-backend/ghl.jsw`
2. Select all, copy
3. Paste into the Wix Studio code editor for `backend/ghl.jsw`
4. Press **Cmd+S** to save

### 1D. Set the GHL Webhook Secret

This is how the backend securely stores the webhook URL without hardcoding it.

1. In Wix Studio, go to **Settings** (gear icon in left sidebar)
2. Click **Secrets Manager**
3. Click **+ New Secret**
4. Fill in:
   - **Name:** `GHL_WEBHOOK_URL`
   - **Value:** `https://services.leadconnectorhq.com/hooks/UJDIrAYT4M5omfYGthyJ/webhook-trigger/a72f86e0-76a1-4489-a3d6-6dccb8f55e94`
5. Click **Save**

### 1E. Test the backend (optional but recommended)

After the site is published to staging, you can test the webhook by calling `saveDreamSubmission()` from a frontend test page or by submitting the Dream Center form.

---

## STEP 2 — Create All 47 Pages

Wix doesn't support creating pages via REST API — each page must be added in the editor. Below are all 47 pages with their exact URL slugs.

**How to add a page:**
1. In Wix Studio, click the **Pages** icon in the left sidebar
2. Click **+ Add Page** (or the `+` next to "Pages")
3. Choose a blank layout or the closest template
4. After the page is created, click the page name → **Page Settings** → **SEO** → set the **Page URL** to the exact slug listed below
5. Set the **Page Title** and **Meta Description** as listed

---

### Core Pages (12) — Do These First

| Route | Page Title | Meta Description |
|---|---|---|
| `/` | Luxury Pool Builder in Gilbert, AZ \| Arise Pools & Landscaping | Arizona's premier luxury pool and landscape design-build company. 15+ years, 200+ projects, East Valley's most awarded team. |
| `/dream-center` | Design Your Dream Backyard \| Arise Dream Center | Use our interactive configurator to design your custom pool or backyard and get an instant investment estimate. |
| `/portfolio` | Project Portfolio \| Arise Pools & Landscaping | Browse our portfolio of luxury custom pools, landscaping, and outdoor living projects across Gilbert, Scottsdale, and the East Valley. |
| `/about` | About Arise Pools & Landscaping \| Our Story | Meet the Arise team. 15+ years of luxury pool and landscape design in the East Valley. Learn our story, our standard, and our values. |
| `/process` | The Arise Method \| Our 7-Step Build Process | From discovery call to reveal day — our proven 7-step process for custom pool and landscape projects with zero surprises. |
| `/financing` | Pool Financing \| Flexible Payment Options \| Arise Pools | Finance your dream backyard with home improvement loans starting as low as $612/mo. Partnering with Monterey Financial and Enhancify. |
| `/reviews` | Client Reviews \| Arise Pools & Landscaping | Read 5-star Google reviews from homeowners across Gilbert, Chandler, Scottsdale, and the East Valley. See what our clients say. |
| `/contact` | Contact Arise Pools & Landscaping | Get in touch with our design team. Schedule a free consultation, call us, or use our contact form. We serve the entire East Valley. |
| `/guide/dream-backyard-playbook` | Free: The Arizona Dream Backyard Playbook \| Arise Pools | Download our free guide to planning your perfect Arizona backyard — pools, landscaping, outdoor living, and financing in one PDF. |
| `/press` | Press & Awards \| Arise Pools & Landscaping | Media mentions, industry awards, and association memberships. Arise Pools & Landscaping recognized across Arizona. |
| `/careers` | Join Our Team \| Careers at Arise Pools | We're building something special. Join the Arise Pools team as a crew member, project manager, or design consultant. |
| `/referral-program` | Referral Program \| Earn Rewards with Arise Pools | Refer a friend and earn $500 in credit or a free quarter of maintenance. Our way of saying thank you to our Arise family. |

---

### Service Pillar Pages (8)

| Route | Page Title | Meta Description |
|---|---|---|
| `/custom-pools` | Custom Pool Builder in Arizona \| Arise Pools | Luxury custom pool design and construction across the East Valley. Geometric, freeform, infinity edge, and plunge pools. |
| `/landscaping` | Landscape Design & Installation \| Arise Pools | Transform your Arizona backyard with desert-modern landscaping, tropical oasis designs, and sustainable planting by Arise. |
| `/hardscape` | Hardscape Design \| Pavers, Flagstone & Walls \| Arise Pools | Custom hardscape design and installation — pavers, flagstone, retaining walls, and decorative concrete across the East Valley. |
| `/remodels` | Pool Remodeling & Resurfacing \| Arise Pools | Breathe new life into your pool. We handle complete pool remodels, resurfacing, equipment upgrades, and water feature additions. |
| `/outdoor-living` | Outdoor Living Design \| Kitchens, Pergolas & More | Custom outdoor kitchens, pergolas, ramadas, and pavilions designed and built by Arise Pools across the East Valley. |
| `/water-fire-features` | Water & Fire Features \| Arise Pools & Landscaping | Custom fire bowls, gas fire features, waterfalls, fountains, and water walls — luxury additions for any Arizona backyard. |
| `/pool-maintenance` | Pool Maintenance Service \| Weekly & Monthly Plans | Weekly and monthly pool cleaning, chemical balancing, and repair service. Keep your Arise pool pristine year-round. |
| `/smart-pool` | Smart Pool Automation \| Arise Pools \| Pentair & Jandy | Control your pool from your phone. LED lighting, automated chemistry, and IoT integration. We install and configure all major brands. |

---

### Service Sub-Pages (8)

| Route | Page Title | Meta Description |
|---|---|---|
| `/custom-pools/geometric` | Geometric Pool Design \| Arise Pools | Modern rectangular and geometric pool designs with clean lines and luxury finishes. Serving Gilbert, Scottsdale, and the East Valley. |
| `/custom-pools/freeform` | Freeform Pool Design \| Natural Lagoons \| Arise Pools | Natural freeform pools with rock features, grottos, and tropical landscaping. Custom designs built across the East Valley. |
| `/custom-pools/infinity-edge` | Infinity Edge Pool Builder \| Arise Pools | Stunning vanishing-edge pool design and construction. Our specialty. Serving Paradise Valley, Scottsdale, and the East Valley. |
| `/custom-pools/plunge-pools` | Plunge Pool & Cold Plunge Builder \| Arise Pools | Small-footprint luxury plunge pools and cold plunge installations for Arizona backyards. Design, build, and maintenance. |
| `/custom-pools/spa-integration` | Pool & Spa Combinations \| Arise Pools | Custom spa-pool combinations with spillover jets, integrated heating, and automated controls. Design-build by Arise. |
| `/landscaping/desert-modern` | Desert Modern Landscape Design \| Arise Pools | Signature low-water desert-modern landscaping for Arizona homes. Drought-tolerant plants, decomposed granite, and clean-line design. |
| `/landscaping/tropical-oasis` | Tropical Oasis Landscape Design \| Arise Pools | Lush, tropical backyard escape designs for Arizona. Palm trees, tropical planting, and resort-style pools. |
| `/outdoor-living/outdoor-kitchens` | Outdoor Kitchen Builder \| Arise Pools \| East Valley AZ | Custom outdoor kitchen design and construction — islands, grills, refrigerators, pizza ovens, and shade structures. |

---

### City Landing Pages (9)

> **Important:** These pages need 800+ words of original, localized copy each. SEO structure and content are specified in Part C of the Master Blueprint.

| Route | Page Title | Meta Description |
|---|---|---|
| `/pool-builder/gilbert-az` | Pool Builder in Gilbert, AZ \| Arise Pools (HQ) | Gilbert's premier luxury pool and landscape design-build company. 15+ years serving Gilbert homeowners. Get your free consultation. |
| `/pool-builder/chandler-az` | Pool Builder in Chandler, AZ \| Arise Pools | Custom pools and landscape design in Chandler, Arizona. Arise Pools builds luxury outdoor living spaces across Chandler. |
| `/pool-builder/mesa-az` | Pool Builder in Mesa, AZ \| Arise Pools | Award-winning custom pool and landscape contractor in Mesa, AZ. Luxury builds, premium materials, transparent process. |
| `/pool-builder/scottsdale-az` | Pool Builder in Scottsdale, AZ \| Arise Pools | Scottsdale's luxury pool and outdoor living specialist. Infinity edges, resort-style pools, and premium landscape design. |
| `/pool-builder/queen-creek-az` | Pool Builder in Queen Creek, AZ \| Arise Pools | Custom pool and landscape design in Queen Creek. Arise Pools serves the growing Queen Creek community with luxury builds. |
| `/pool-builder/phoenix-az` | Pool Builder in Phoenix, AZ \| Arise Pools | Phoenix custom pool builder — luxury pools, landscape design, and outdoor living. Serving Phoenix homeowners for 15+ years. |
| `/pool-builder/tempe-az` | Pool Builder in Tempe, AZ \| Arise Pools | Custom pool and landscape design in Tempe, Arizona. Arise Pools brings luxury outdoor living to Tempe homeowners. |
| `/pool-builder/paradise-valley-az` | Pool Builder in Paradise Valley, AZ \| Arise Pools | Paradise Valley's luxury pool specialist. Infinity edges, estate landscapes, and resort-style outdoor living by Arise Pools. |
| `/pool-builder/fountain-hills-az` | Pool Builder in Fountain Hills, AZ \| Arise Pools | Custom pools and luxury landscape design in Fountain Hills. Arise Pools serves Fountain Hills and the surrounding area. |

---

### Blog Category Pages (4 — `/blog` is auto-created by Wix Blog)

When you add the **Wix Blog app**, the `/blog` route is created automatically. You'll also need to configure these 4 category pages:

| Category Slug | Category Name |
|---|---|
| `design` | Design & Inspiration |
| `cost-and-planning` | Cost & Planning |
| `maintenance-tips` | Maintenance Tips |
| `arizona-lifestyle` | Arizona Lifestyle |

**How to create categories:**
1. In Wix Blog → **Categories** tab
2. Add each category with the slug listed above

---

### Legal & System Pages (5)

| Route | Page Title |
|---|---|
| `/privacy` | Privacy Policy \| Arise Pools & Landscaping |
| `/terms` | Terms of Service \| Arise Pools & Landscaping |
| `/accessibility-statement` | Accessibility Statement \| Arise Pools |
| `/sitemap.xml` | Auto-generated by Wix — no action needed |
| `/404` | In Wix Studio: Settings → Error Pages → customize your 404 |

---

## STEP 3 — Set Up the Dream Center Page (`/dream-center`)

The Dream Center is the most important page on the site. It's a 7-step interactive configurator that connects to the `ghl.jsw` backend.

### Option A — Embed as Wix HTML Embed (Recommended for now)

1. On the `/dream-center` page in Wix Studio, add an **HTML iframe** element (Add → Embed → HTML iframe)
2. Expand it to full width/height
3. In the iframe settings, paste the entire contents of:  
   `/Users/jakemedford/Documents/Claude/Projects/Arise Pools/Arise-Dream-Center-Configurator.html`
4. Change the last step's form submission to call `saveDreamSubmission()` via Velo's `wix-window` import

> **Note:** The configurator HTML file was built to run standalone. For the Wix integration, you'll need a small code bridge in the page's frontend code panel to route the form submission to `backend/ghl.jsw`. See the connection code below.

### Page Frontend Code (paste in the `/dream-center` page's code panel)

```javascript
import { saveDreamSubmission } from 'backend/ghl';

// Listen for the form submission message from the embedded HTML iframe
$w.onReady(function () {
  $w('#dreamIframe').onMessage(async (event) => {
    if (event.data.type === 'DREAM_SUBMIT') {
      const result = await saveDreamSubmission(event.data.payload);
      $w('#dreamIframe').postMessage({ type: 'SUBMIT_RESULT', result });
    }
  });
});
```

### Option B — Build Natively in Wix Studio (Best for long-term)

For the full native Wix Studio implementation, each step becomes a Wix multi-state box with:
- State 1–7 = each step of the configurator
- Repeater for feature/add-on selection grids
- Submit button calling `saveDreamSubmission()` directly via Velo imports

This is a larger build — plan 4–6 hours to implement natively. The HTML embed approach gets you live faster and can be swapped out later.

---

## STEP 4 — Navigation & Site Structure

Once pages are created, wire up the navigation:

### Main Nav (Desktop)
```
Home | Services ▾ | Portfolio | About | Reviews | Financing | Contact
```

**Services dropdown:**
- Custom Pools → /custom-pools
- Landscaping → /landscaping
- Hardscape → /hardscape
- Pool Remodels → /remodels
- Outdoor Living → /outdoor-living
- Maintenance → /pool-maintenance
- Smart Pools → /smart-pool

### Footer Nav (3 columns)
**Services:** Custom Pools, Landscaping, Hardscape, Remodels, Outdoor Living, Maintenance, Smart Pools  
**Cities:** Gilbert, Chandler, Mesa, Scottsdale, Queen Creek, Phoenix, Tempe, Paradise Valley, Fountain Hills  
**Company:** About, Process, Portfolio, Reviews, Financing, Referral Program, Blog, Careers, Contact

### Floating CTA Bar
A persistent bar at the bottom of the viewport:  
`📞 (480) XXX-XXXX | Design My Backyard →`

---

## STEP 5 — SEO Settings

In **Settings → SEO** in Wix Studio:

1. **Site title:** `Arise Pools & Landscaping | Luxury Pool Builder in Gilbert, AZ`
2. **Site description:** `Arizona's premier luxury pool and landscape design-build company. Custom pools, outdoor living, and landscape design across the East Valley.`
3. **Favicon:** Upload the Arise logo mark
4. **Social share image:** Upload a hero project photo (1200×630px)
5. **Google Search Console:** Verify via the Wix SEO wizard → Indexing → connect GSC

---

## STEP 6 — Wix Apps to Install

Install these from the Wix App Market before launching:

| App | Purpose | Notes |
|---|---|---|
| **Wix Bookings** | Consultation scheduling | Creates /bookings route automatically |
| **Wix Blog** | Blog platform | Already have 12 posts via API |
| **Wix Forms** | Contact form on /contact | OR use the Dream Center for all lead capture |
| **Wix Chat** (optional) | Live chat widget | Connects to GHL via webhook |
| **Google Analytics** | GA4 tracking | Add via Settings → Integrations |

---

## STEP 7 — Pre-Launch Checklist (Staging)

Before going live, verify each of these on the staging URL:

- [ ] `backend/ghl.jsw` is deployed and `GHL_WEBHOOK_URL` secret is set
- [ ] Dream Center form submits and data appears in GHL + DreamSubmissions CMS
- [ ] All 47 page URLs resolve (no 404s)
- [ ] Navigation links point to correct pages
- [ ] Blog is displaying the 12 published posts
- [ ] Mobile layout reviewed on iPhone (P0 requirement before go-live)
- [ ] All service pages have at least 300+ words of copy
- [ ] City pages have localized H1s and 800+ words
- [ ] `/financing` page has calculator or Monterey/Enhancify embed
- [ ] Google Analytics is firing events
- [ ] Contact form routes to GHL or email
- [ ] Page speed tested via PageSpeed Insights (target: 80+ mobile)

---

## File Reference

| File | Location | Purpose |
|---|---|---|
| `ghl.jsw` | `/wix-velo-backend/ghl.jsw` | Backend GHL integration — deploy to Wix |
| `Arise-Dream-Center-Configurator.html` | `/Arise-Dream-Center-Configurator.html` | 7-step configurator — embed or port to Wix |
| `Arise-Pools-MASTER-Blueprint.md` | `/Arise-Pools-MASTER-Blueprint.md` | Full site spec, content, SEO, design direction |
| This file | `/Wix-Studio-Deployment-Guide.md` | This guide |

---

## Time Estimates

| Task | Estimated Time |
|---|---|
| Deploy ghl.jsw + set Secret | 10 min |
| Create all 47 pages (blank, URLs set) | 1.5–2 hrs |
| Wire navigation | 30 min |
| Embed Dream Center configurator | 30 min |
| SEO settings + Wix apps | 30 min |
| **Total manual setup** | **~3–4 hours** |

Content writing (city pages, service pages) is separate and can be done progressively post-launch.

---

*Last updated: May 2026 | Staging only — do not publish to production until mobile review is complete.*
