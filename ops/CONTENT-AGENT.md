# Arise Content Agent: Runbook

One process for every project photo, gallery and blog post on arisepal.com, so every system (site, blog, funnel, GHL social, ads, Hermes, Notion) refers to the same projects by the same names.

Repo is PUBLIC. Creative project names only. Client surnames live only in the private map in `ClaudeCode-Master/Clients/Arise Pool and Landscaping/CLAUDE.md`.

## Sources of truth

| File | What it holds | Who writes it |
|---|---|---|
| `data/projects.json` | Every project: slug, creative name, city, neighborhood, tagline, styles, blurb, photos + alt text, cover, status, which posts feature it | Intake step and blog step |
| `data/content-rotation.json` | City list with neighborhoods, rotation state, post history | `scripts/content-next.py --record` only |
| `js/portfolio-gallery.js` | Gallery data block (generated) | `scripts/projects-sync.py` only |
| `oasis.html` | Funnel. Curated, hand-built. Do not regenerate or touch its form/webhook code | Humans, on request |

Never hand-edit the generated block. Edit `data/projects.json`, then run `python3 scripts/projects-sync.py`.

## Naming Function

Every project gets a creative name before anything is published. Once a name is live it never changes, because posts, ads and galleries link to it.

1. **Name**: 2 to 3 words, Title Case, built from what the photos show (mood, signature feature, lifestyle). Patterns in use:
   - "The [Adjective] [Escape/Jewel/Retreat]": The Desert Escape, The Hidden Jewel, The Modern Escape
   - "[Value] [Living/Focused]": Legacy Living, Family Focused
   - "[Quality] [Noun]": Sleek Opulence, Layered Confidence, Elevated Entertainment
   - Never a surname, street, address, HOA or city alone. Must be unique in the registry.
2. **Tagline**: 2 words naming the style or payoff: Luxury Outdoor Living, Modern Makeover, Ultimate Oasis.
3. **Slug**: kebab-case of the name: `the-desert-escape`.
4. **Photo files**: `/images/projects/{slug}/{slug}-{city}-az-{NN}-{1800|900}.jpg` (the intake script does this).
5. **Alt text**: what is in the shot, plain and specific, no "image of": "Pool with sheer water features at dusk". The site appends ", {Name} in {City}, AZ".
6. **Blurb**: one sentence, only what the photos show. No prices, timelines, client names or claims you can't see.
7. **How every system refers to it**: "{Name} in {City}" (e.g. "The Hidden Jewel in Gilbert"), linked to `/portfolio#{slug}` (opens that gallery directly).

## A. New project intake

Trigger: a new subfolder appears in Jared's Drive folder `114tsgW_kGn0eckE0TEPxe_XBAOBqs5SD` (folders are named by client surname, e.g. "Workman Pictures").

1. Look up the surname in the private map. If the project already has a creative name (the 7 pending tiles do), use it. If not, pick one with the Naming Function and add it to the private map.
2. Download the folder's images into a fresh empty dir (Drive direct download: `https://drive.usercontent.google.com/download?id=ID&export=download&confirm=t`).
3. `python3 -I scripts/project-intake.py --src DIR --slug SLUG --name "NAME" --city "CITY" --tagline "TAGLINE"`
4. Open the contact sheet it prints. In `data/projects.json`: order photos best-first, write a real alt for each, set `cover`, `styles`, `blurb`, `neighborhood` if known, then `status: "live"`.
5. Portfolio tile: if the project already has a tile, add `data-project="SLUG"` and point its img at the 900px cover. If new, add a tile in the same markup.
6. `python3 scripts/projects-sync.py` must print OK. Commit, push, verify `/portfolio#SLUG` opens the gallery live.

## B. Weekly blog post

1. `git pull --ff-only`, then `python3 scripts/content-next.py` and follow its output exactly:
   - `focus: city` -> a city post ("Custom Pool Builder in Gilbert, AZ" style angle).
   - `focus: neighborhood` -> a neighborhood post for that neighborhood in that city.
   - Feature `featuredProject` by name with 2 to 3 of its photos inline and a link to its gallery.
2. Neighborhood names are targets, not facts. Any specific claim (HOA rules, lot sizes, build era, amenities) must be verified with agent-reach research first, or left out.
3. Write per the template rules in the scheduled task (structure, JSON-LD, internal links, Pentair only, phone (623) 292-3073). Link the city page, the featured project's gallery, and `/oasis` as the primary CTA. Zero em-dashes. Run the humanizer pass on the copy.
4. Wire it in (blog.html card, category page card, sitemap), validate, push, verify live 200.
5. Only after it is live: `python3 scripts/content-next.py --record POST-SLUG`, then commit and push the updated `data/*.json`.

## C. Leave alone

- Funnel `/oasis` posts straight to GHL webhook `eea6dd51` with an n8n sheet backup. Don't change the form, the webhook or `/book`.
- `js/site.js` and the site-wide contact form webhook.
- Existing published posts, images, and project names.
