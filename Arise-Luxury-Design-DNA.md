# Arise Luxury Landing — Design DNA Extraction

Extracted from `/arise-luxury/` codebase. This is the proven design Jacob's client loves. Every Wix page must match these patterns exactly.

---

## 1. Token System (exact values)

### Colors (HSL CSS vars)
| Token | HSL | Hex equiv | Usage |
|---|---|---|---|
| `--cream` | 37 33% 96% | #F7F1E8 | Page background |
| `--stone` | 30 10% 9% | #1A1814 | Primary text, dark sections |
| `--gold` | 37 42% 61% | #C9A464 | Primary accent, CTAs, borders, icons |
| `--gold-light` | 37 55% 80% | #E5CB9A | Hero italic emphasis, hairlines, hover |
| `--gold-dark` | 40 75% 31% | #8B6914 | AA-compliant gold-on-cream text |
| `--pool-blue` | 196 66% 32% | #1C738A | Accent secondary |
| `--pool-deep` | 203 62% 13% | #0C2736 | Dark CTA bands (CTASection bg) |
| `--slate` | 30 6% 16% | #2E2A25 | Nav CTA bg, secondary buttons |
| `--mist` | 25 4% 52% | #8A8480 | Muted body text |

### Typography
- **Display:** Cormorant Garamond — weights 300 (light), 400, italic 300, italic 400
- **Body:** Jost — weights 300, 400, 500, 600
- Google Fonts import: `Cormorant+Garamond:ital,wght@0,300;0,400;1,300;1,400&family=Jost:wght@300;400;500;600`

### Type Scale
| Element | Font | Weight | Size | Tracking | Color |
|---|---|---|---|---|---|
| H1 hero | Cormorant | light (300) | clamp(2.8rem, 5.5vw, 5.5rem) | — | white/95 |
| H1 italic accent | Cormorant italic | — | inherited | — | gold-light |
| H2 section | Cormorant | light | 4xl / 5xl | tracking-wide | stone |
| Eyebrow | Jost | medium (500) | 0.65rem | 0.3em | gold |
| Body | Jost | light (300) | 1.05rem | — | stone/60–80 |
| Nav links | Jost | medium | 0.7rem | 0.18em | stone/80 |
| CTA buttons | Jost | semibold (600) | 0.75rem / 0.7rem | 0.15–0.2em | stone on gold |
| Form labels | Jost | — | xs | 0.15em | foreground/70 |
| Footer body | Jost | — | sm | — | cream/60 |
| Footer subtext | Jost | — | xs | — | cream/40 |

### Spacing
- Section padding: `py-24 md:py-32` (96px → 128px desktop)
- Max content width: `max-w-[1200px]` (1400px for hero/portfolio)
- Container padding: `px-6 md:px-20` (hero), `px-6` elsewhere
- Card padding: `p-8`
- Grid gap: `gap-6` to `gap-8`

### Radius
- Global: `--radius: 0.25rem` (4px) — effectively sharp
- Buttons: NO border-radius (sharp edges, no `rounded-full`)
- Form inputs: `rounded-none`
- Slide indicators: `rounded-full` (exception — dots only)

### Borders & Dividers
- Hairlines: `border-gold/10`, `border-gold/15`, `border-gold/20`
- Section dividers: `w-16 h-px bg-gold mx-auto mt-6` (centered gold rule, 64px wide)
- Eyebrow dividers: `w-10 h-[1px] bg-gold` — flanking text, horizontal
- Card hover: `hover:border-gold hover:shadow-lg hover:-translate-y-1`
- Bottom reveal line: `h-[2px] bg-gold scale-x-0 group-hover:scale-x-100` (Dream Center cards)

### Shadows & Effects
- Cards: `hover:shadow-lg` only (no default shadows)
- No gradients on cards or sections
- Hero overlay: `linear-gradient(135deg, rgba(13,37,53,0.82) 0%, rgba(27,107,138,0.55) 100%)`
- Page hero overlay: `linear-gradient(135deg, rgba(13,37,53,0.85) 0%, rgba(27,107,138,0.6) 100%)`
- Portfolio hover: `bg-gradient-to-t from-black/70 via-transparent to-transparent`

---

## 2. Component Patterns

### Navigation
- Fixed top, cream/95 bg + backdrop-blur-md
- Border bottom: `border-gold/20`
- Logo: `ARISE & CO.` — Cormorant, 1.25rem, tracking 0.15em, & in gold
- Links: Jost medium, 0.7rem, uppercase, tracking 0.18em, foreground/80 → gold on hover
- Services dropdown: AnimatePresence, gold/15 border, min-w 200px
- CTA button: `bg-secondary text-secondary-foreground` (slate bg, cream text), "Begin Your Design"
- Mobile: hamburger → accordion services, full CTA pinned bottom

### Hero (Homepage)
- Full-bleed `min-h-screen`, 3-slide auto-rotate @ 5.5s
- AnimatePresence sync mode for crossfade (1.2s)
- Content: eyebrow (gold hairline + Jost micro text) → H1 (Cormorant light, last word italic gold-light) → subtitle (Jost light, white/75) → 2 CTAs
- Primary CTA: gold bg, stone text, sharp
- Ghost CTA: white/30 border, white/85 text → gold/gold-light on hover
- Stats bar: bottom-right on desktop (hidden mobile), 3 items, Cormorant 3xl gold-light values, micro Jost labels
- Slide dots: bottom center, gold active, white/40 inactive

### Eyebrow Pattern
Used on every section:
```
<div className="flex items-center justify-center gap-4 mb-6">
  <div className="w-10 h-[1px] bg-gold" />
  <span className="font-body font-medium text-[0.65rem] uppercase tracking-[0.3em] text-gold">Label</span>
  <div className="w-10 h-[1px] bg-gold" />
</div>
```
Variant without flanking lines: just `text-gold text-xs uppercase tracking-[0.3em] mb-4`

### Section Heading Pattern
```
eyebrow (gold, micro, uppercase, 0.3em tracking)
H2 (Cormorant light, 4xl/5xl, stone, tracking-wide)
optional subtitle (Jost, stone/60, max-w, leading-relaxed)
gold rule (w-16 h-px bg-gold mx-auto mt-6)
```

### Card Pattern (Services / Dream Center)
- White or cream/50 bg, `border border-gold/10` (or stone/10)
- `p-8`, no radius
- Icon: lucide, `w-8 h-8 text-gold`, scale 110% on hover
- Title: Cormorant, text-xl, tracking-wide
- Body: Jost, text-sm, stone/55–60, leading-relaxed
- Hover: `border-gold/30`, shadow-lg, slight lift (-translate-y-1)
- Dream Center special: gold bottom-line reveal (scale-x 0→100%)

### Portfolio Grid
- 3 columns lg, 2 sm, 1 mobile
- Aspect ratio 4:3
- Image scale 110% on hover (duration-700)
- Overlay: gradient from-black/70, opacity 0→100% on hover
- Caption: Cormorant title + Jost gold category, translate-y slide up

### Testimonial Cards
- 2-column grid
- Gold/15 border, cream/50 bg, p-8
- Gold stars (Star lucide, fill-gold text-gold, w-4)
- Quote: Jost italic, foreground/80, sm, relaxed
- Name: Cormorant, lg
- Location: Jost, xs, uppercase, tracking 0.15em, muted

### CTA Section (Closing Band)
- `bg-pool-deep text-cream`
- Centered, max-w 800px
- H2: Cormorant light, 3xl/5xl, tracking-wide
- Subtitle: cream/60, sm
- CTA: gold bg, stone text, Jost semibold, xs, uppercase, tracking 0.2em, sharp
- Hover: gold → gold-light

### Page Hero (Interior pages)
- 50vh, min-h 400px
- Same gradient overlay as homepage
- Eyebrow + H1 + optional subtitle
- Content max-w 1200px

### Lead Form
- Zod + react-hook-form + shadcn Form
- Inputs: `rounded-none h-12`, border-gold/20, focus:border-gold
- Labels: Jost xs, uppercase, tracking 0.15em, foreground/70
- Submit: full-width gold bg, stone text, Jost semibold
- Success: "✓ Received" eyebrow → "Thank You" H2 → message

### Footer
- `bg-stone text-cream/80`
- 4-column grid (brand / services / company / contact)
- Logo: Cormorant 2xl, cream, & in gold
- Section heads: Jost xs, uppercase, tracking 0.2em, text-gold
- Links: Jost sm, cream/60 → gold on hover
- ROC: cream/40, xs
- Contact: lucide icons (Phone, Mail, MapPin) w-4 text-gold
- Hours: separate block under contact
- Bottom bar: border-t cream/10, xs, cream/30, flex between

---

## 3. Animation Patterns (Framer Motion)

| Pattern | Initial | Animate | Timing |
|---|---|---|---|
| Section fade-up | opacity:0, y:30 | opacity:1, y:0 | duration: 0.8, once, margin -100px |
| Card stagger | opacity:0, y:30–40 | opacity:1, y:0 | duration: 0.5–0.6, delay: i*0.08–0.1 |
| Hero slide | opacity:0 | opacity:1 | duration: 1.2, ease: easeInOut |
| Hero content | opacity:0, y:30 | opacity:1, y:0 | duration: 0.7, mode: wait |
| Eyebrow slide-in | opacity:0, x:-20 | opacity:1, x:0 | duration: 0.6–0.8 |
| Dropdown | opacity:0, y:8 | opacity:1, y:0 | duration: 0.2 |
| Portfolio filter | opacity:0, scale:0.9 | opacity:1, scale:1 | duration: 0.4, popLayout |

All animations use `viewport={{ once: true }}` — fire once, don't replay.

---

## 4. Homepage Section Order

1. **Hero** — full-bleed 3-slide, stats bar, 2 CTAs
2. **Dream Center** — 6-category card grid with icons (current: static links, target: 7-step configurator)
3. **Services** — 6-card grid
4. **Testimonials** — 4-card 2-col grid
5. **CTA Section** — pool-deep band, centered

**Expansion for 49-page structure** (per Master Blueprint): insert Trust Bar after Hero, Signature Work after Dream Center, Arise Method after Services, Founder Moment + Review Wall + City Grid + Financing Strip before Closing CTA.

---

## 5. Existing Routes (13) → 49-page expansion

Current: /, /custom-pools, /landscaping, /remodels, /maintenance, /outdoor-living, /portfolio, /portfolio/:slug, /financing, /about, /contact, /blog, /blog/:slug, 404.

Add: Dream Center (/dream-center), Signature Work (/signature-work), Arise Method (/the-arise-method), Reviews (/reviews), Warranty (/warranty), Careers (/careers), Consultation Booking (/consultation), 3 new service pillars (Hardscape, Outdoor Structures, Water & Fire Features), 8 signature styles, 11 city pages, 3 legal pages.

---

## 6. Image References

Images use `/images/client/` paths:
- hero-banner.jpg — cinematic pool aerial
- about.jpg — team/founder
- landscape.jpg — desert landscape project
- services-bg.jpg — outdoor living
- pool-design.jpg — 3D pool rendering
- project-support.jpg — hardscape/patio

Project images: `/images/projects/gilbert-remodel/01–10.jpg`

These are the real client photos to extract and push to Wix media library.
