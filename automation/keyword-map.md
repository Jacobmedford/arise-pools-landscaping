# Keyword Map

Reference for the blog automation cron (see `BLOG-AUTOMATION.md` and `topic-queue.json`). Lists every keyword or head term already "owned" by an existing page, so new posts never cannibalize a money page, a city page, or an existing article. If a candidate topic's keyword overlaps anything below, skip it and take the next queued item.

## Money pages (service pages) — own the head terms

- `/services/custom-pools` — custom pool builder, custom pool design, custom pool construction
- `/services/custom-pools/geometric` — geometric pool design
- `/services/custom-pools/freeform` — freeform pool design
- `/services/custom-pools/infinity-edge` — infinity edge pool, infinity pool
- `/services/custom-pools/plunge-pools` — plunge pool, cocktail pool
- `/services/custom-pools/spa-integration` — pool and spa combo
- `/services/landscape-design` — landscape design
- `/services/landscape-design/desert-modern` — desert modern landscaping
- `/services/landscape-design/tropical-oasis` — tropical backyard landscaping
- `/services/pool-remodels` — pool remodel, pool renovation
- `/services/outdoor-living` — outdoor living spaces
- `/services/outdoor-living/outdoor-kitchens` — outdoor kitchen design
- `/services/hardscape` — hardscape, sport courts
- `/services/water-fire-features` — water features, fire features
- `/services/pool-maintenance` — pool maintenance, pool service
- `/services/smart-pool` — smart pool automation
- `/configurator` and `/guide` — "design my pool," planning tool intent

## City pages — own "[service] in [city]" head terms

Do not target the bare head term "pool builder in <city>" or "landscape design <city>" for any of these; the city page already owns it. A blog post about the same city is fine as long as the angle is a distinct sub-topic (cost, permits, seasonal, HOA, lot type, maintenance), not the head term itself.

- `/cities/phoenix`, `/cities/scottsdale`, `/cities/paradise-valley`, `/cities/mesa`, `/cities/gilbert`, `/cities/chandler`, `/cities/tempe`, `/cities/queen-creek`, `/cities/san-tan-valley`, `/cities/fountain-hills`, `/cities/cave-creek`

## Existing blog posts — do not repeat these angles

| Slug | Category | Owned angle / keyword |
|---|---|---|
| `arizona-backyard-shade-ramadas-and-pergolas` | Arizona Lifestyle | ramadas vs pergolas vs shade sails in Arizona |
| `hard-water-and-calcium-scale-on-arizona-pools` | Maintenance Tips | calcium scale / hard water on Arizona pools |
| `infinity-edge-pools-for-arizona-hillside-lots` | Design & Inspiration | infinity edge pools on hillside lots |
| `pool-permits-and-hoa-approval-in-scottsdale` | Cost & Planning | pool permits and HOA approval, Scottsdale |
| `what-a-125k-pool-actually-gets-you-2026` | Cost & Planning | $125k pool budget breakdown |
| `12-pool-shapes-for-arizona-lots-under-quarter-acre` | Design & Inspiration | pool shapes for small/compact lots |
| `monsoon-pool-recovery-checklist` | Maintenance Tips | post-monsoon pool recovery |
| `designing-for-monsoon-dust-and-115-degree-summers` | Arizona Lifestyle | designing for monsoon dust and extreme heat |

## The four blog categories

Every post must map to exactly one of the four existing category pages (do not invent new categories, do not create new `blog/category/*.html` files):

- `design` → Design & Inspiration
- `cost-and-planning` → Cost & Planning
- `maintenance-tips` → Maintenance Tips
- `arizona-lifestyle` → Arizona Lifestyle

## Local relevance rule

Every post should read as written for the East Valley / Phoenix metro, and should name-check at least one or two of the eleven service-area cities in the prose (not just the title) — but only as supporting local color and internal links, never by repeating a city page's own head term.
