# Blog Automation Playbook

The engine that publishes one distinct, SEO-rich, internally linked blog post a week to arisepal.com, targeting Arizona local-search intent (pools, landscaping, and outdoor living by service and by East Valley city) without cannibalizing the money pages, the city pages, or the existing 8 posts. Zero em-dashes by rule. Read `keyword-map.md` and `topic-queue.json` alongside this.

Runs as a Claude Code Routine on **Claude Sonnet 5**, in a fresh cloud session, fully unattended. There is no human in the loop: the run must commit and push directly to `main` and never wait on a pull request or approval. This site is deployed as static HTML with `outputDirectory: "."` in `vercel.json` (no build step), so Vercel auto-deploys `main` on push — a successful push is the publish.

## Schedule

- Once a week, Monday 8:00 AM Arizona time (Arizona has no DST, so this is a fixed `15:00 UTC`). Cron: `0 15 * * 1`.
- Each run publishes exactly one post and pulls the next angle from `topic-queue.json`.

## Site architecture (read this before writing anything)

This is a static multi-page site, **not** a templated CMS. There is no `posts.json` and no dynamic `[slug]` route. A new post touches exactly four files:

1. A brand-new `blog/<slug>.html` file — the post itself.
2. `blog.html` — the "New & Noteworthy" grid on the blog index.
3. `blog/category/<category>.html` — the matching category page's "Latest Articles" grid.
4. `sitemap.xml` — one new `<url><loc>...</loc></url>` line.

Never edit `blog/category/*.html` to add a category that doesn't exist. Never touch `index.html`, any `/services/*` page, any `/cities/*` page, `contact.html`, or any JS/analytics file.

## Building the post file

Do not invent new markup or CSS. Copy the full HTML of an existing post in `blog/` (any one of the 8) as the literal starting point, keeping the `<nav>`, mobile drawer, sticky CTAs, and `<footer>` byte-for-byte identical. Then change only:

- `<title>`, meta `description`, canonical URL, all `og:*` and `twitter:*` tags, to match the new post.
- The `BlogPosting` JSON-LD block: `headline`, `description`, `image`, `datePublished`, `dateModified`, `articleSection` (the category name), `mainEntityOfPage`.
- The `FAQPage` JSON-LD block: 3 to 4 question/answer pairs matching the `.post-faq` `<dl>` at the end of the post body.
- The `HomeAndConstructionBusiness` JSON-LD block: leave exactly as-is, copied verbatim from the source post.
- The hero background image: reuse an existing path under `/images-for-web-or-mls/`, `/images-for-web-or-mls-2/`, or `/images-for-web-or-mls-3/` that fits the topic (check what nearby posts use for the same category). Never invent an image path that doesn't exist in the repo.
- The eyebrow line (`Blog · <Category Name>`), `<h1>`, and the hero subtitle (`<Month Day, Year> · <N>-minute read`).
- The `.post-body` content and the closing `.post-faq` block.

### Post content shape (SEO-rich, keyword-rich, still genuinely useful)

- Open with a short paragraph that states the topic plainly and names the target keyword's intent in the first two sentences.
- 3 to 5 `<h2>` sections. Use natural question-style or benefit-style headings that match how people actually search ("How much does...", "What to know before...", "The X vs Y difference").
- Short, entity-rich paragraphs. Use a list (`<ul>`/`<ol>`) where it helps a reader scan.
- Weave in 2 to 3 internal links from the topic's `internalLinks` (the relevant service or city page) plus 1 to 2 links to related existing posts, matched by category.
- Work in the topic's `localFocus` city (if set) naturally in the prose — not just the title — along with one or two of the other ten East Valley cities where it fits naturally. Never repeat a city page's own head term ("pool builder in <city>"); write about the specific angle instead (cost, permits, HOA, lot type, seasonal, maintenance).
- Close with a short `<h2>Questions We Hear About...</h2>` section holding the `.post-faq` `<dl>` (3 to 4 Q&A pairs), then a closing sentence that leads into booking a consultation, immediately before the shared `.cta-section` block.
- Length: 700 to 1,200 words. Quality over length. Never pad, never fabricate prices, awards, certifications, or testimonials. Canonical facts only (licensed & bonded, ROC# 342276 commercial / ROC# 342277 residential, 15+ years, East Valley service area).

## Publish flow (what the routine does each run)

1. Pull the latest repo so the run builds on current state.
2. Load `topic-queue.json`. Take the oldest item with status `queued`. If fewer than 8 remain queued, generate 6 to 10 fresh angles in the spirit of `keyword-map.md` (vary category and city so consecutive posts do not repeat the same city or category two weeks running) and append them first.
3. Cross-check the chosen keyword against `keyword-map.md`. If it overlaps a money page, a city page, or an existing post's angle, skip it (mark `skipped`) and take the next queued item.
4. Write `blog/<slug>.html` per the structure above. Pick 1 to 2 related posts for internal links by matching `category`.
5. Add the new card as the **first** card inside the `.services-grid` under "New & Noteworthy" in `blog.html`, matching the existing card markup exactly (image, date line, `<h3>` title, one-sentence teaser, `.bottom-line`).
6. Add the same card as the **first** card inside the `.services-grid` under "Latest Articles" in the matching `blog/category/<category>.html`.
7. Add `<url><loc>https://www.arisepal.com/blog/<slug></loc></url>` to `sitemap.xml`, grouped with the other blog post URLs.
8. Set the queue item's status to `published` with its `slug` and `date`.
9. Validate: `topic-queue.json` still parses, the new slug is unique across `blog/`, every `internalLinks` path resolves to a real route in the repo, the post has at least 3 `<h2>`s and a populated `.post-faq` block, and there are zero em-dashes anywhere in the new content.
10. Since there is no build step, spot-check the new HTML file is well-formed (matching `<head>`/`<body>`/`<html>` tag balance) rather than running a build.
11. Commit the four changed/added files with a message ending in the Co-Authored-By line, then push directly to `origin main`. Do not open a pull request and do not pause for approval; this recurring content task is pre-authorized to publish straight to `main`.
12. Wait about 60 seconds, then verify the live URL (`https://www.arisepal.com/blog/<slug>`) returns 200.
13. End with a short summary: title, keyword, live URL, category, word count, validations passed.

## Internal backlinking (the structure)

- Every post links to 1 to 2 money or city pages (from the topic's `internalLinks`) and 1 to 2 related posts.
- The blog index and category pages surface the new post immediately because step 5 and 6 add it directly to their grids.
- `sitemap.xml` is hand-maintained on this site (no build-time generation), so step 7 is required every run.

## Safety and quality gates

- Never repeat a topic or target an owned keyword. The queue plus keyword-map enforce this.
- Never fabricate prices, stats, awards, or testimonials.
- Never force-push, never delete or edit existing posts, never touch `/services/*`, `/cities/*`, `contact.html`, `vercel.json`, or any analytics ID.
- If validation or the push fails, stop and report plainly. Do not publish a broken or half-written post.
- Zero em-dashes anywhere in the output.

## Volume note

One post a week is about 4 a month, roughly 50 a year. The queue plus the generate-more step can sustain this indefinitely at that pace. If distinct, genuinely useful local angles get thin, slow the cadence rather than pad — this is a deliberate choice to revisit, not a hard commitment.
