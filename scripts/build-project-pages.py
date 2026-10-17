#!/usr/bin/env python3
"""Build one indexable page per live portfolio project from data/projects.json.

- Writes portfolio/<slug>.html for every project with status "live" (Vercel cleanUrls serves
  it at /portfolio/<slug>). Files are only rewritten when their content changes.
- Writes portfolio/sitemap-images.json: each project page URL with every image URL + caption,
  for the sitemap step to read.
- Copies the GA4 snippet, stylesheet links, favicon links, nav + mobile drawer + sticky CTA bar,
  footer and the shared script tags from index.html at build time, so the pages stay in step.
- Uses these optional registry fields when present: story (list of paragraph strings),
  features (list of {title, text}), services (list of service slugs, e.g. "custom-pools").
- Path rules (photo files, full-size lightbox file) come from scripts/projects-sync.py.
- Never deletes anything: a page whose project is no longer live is reported, not removed.

Usage: python3 scripts/build-project-pages.py [--check]   (--check = validate only, write nothing)
"""
import html, importlib.util, json, os, re, struct, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REG = os.path.join(ROOT, 'data', 'projects.json')
INDEX = os.path.join(ROOT, 'index.html')
OUT_DIR = os.path.join(ROOT, 'portfolio')
SITEMAP_JSON = os.path.join(OUT_DIR, 'sitemap-images.json')
SITE = 'https://www.arisepal.com'
BUSINESS = {'@type': 'HomeAndConstructionBusiness', '@id': SITE + '/#business', 'name': 'Arise Pools & Landscaping', 'url': SITE + '/'}
PROJECT_CSS = '<link rel="stylesheet" href="/css/gh-project.css?v=20261016">'
EM_DASH = chr(0x2014)  # the character must never appear in generated copy

_spec = importlib.util.spec_from_file_location('projects_sync', os.path.join(ROOT, 'scripts', 'projects-sync.py'))
sync = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sync)

SERVICES = {
    'custom-pools': ('Custom Pools', 'Geometric, freeform and infinity-edge pools designed around the home and the lot.'),
    'landscape-design': ('Landscape Design', 'Desert modern to resort lush, planted for the Arizona climate.'),
    'pool-remodels': ('Pool Remodels', 'Resurfacing, tile, lighting and full redesigns for an existing pool.'),
    'outdoor-living': ('Outdoor Living', 'Outdoor kitchens, bars, pergolas and covered rooms for living outside.'),
    'hardscape': ('Hardscape & Sport Courts', 'Travertine and paver decks, walls, steps, putting greens and sport courts.'),
    'water-fire-features': ('Water & Fire Features', 'Sheer descents, scuppers, spillovers, fire pits and fire tables.'),
    'pool-maintenance': ('Pool & Landscape Maintenance', 'Ongoing care for the pool and landscape after the build.'),
    'smart-pool': ('Smart Automation & Cleaning Systems', 'Automation, lighting control and cleaning systems.'),
}
CITIES = {
    'gilbert': 'Gilbert', 'chandler': 'Chandler', 'mesa': 'Mesa', 'scottsdale': 'Scottsdale',
    'queen-creek': 'Queen Creek', 'phoenix': 'Phoenix', 'tempe': 'Tempe', 'paradise-valley': 'Paradise Valley',
    'fountain-hills': 'Fountain Hills', 'cave-creek': 'Cave Creek', 'san-tan-valley': 'San Tan Valley',
}
# Projects outside a city we have a page for: an honest "near" line plus the closest city pages.
NEARBY = {
    'superstition-mountains': ('in the Superstition Mountains area, east of Mesa', ['mesa', 'queen-creek']),
    'gold-canyon': ('in Gold Canyon, east of Mesa', ['mesa', 'queen-creek']),
}
HQ_CITY = 'san-tan-valley'

SURVEY_BAND = ('<div class="section gh-night" id="start-project"><div class="gh-moon" aria-hidden="true"></div>'
               '<div class="section-inner"><div class="section-heading"><div class="eyebrow"><div class="eyebrow-line"></div>'
               '<span class="eyebrow-text">Start Your Project</span><div class="eyebrow-line"></div></div>'
               '<h2>Want a Backyard <em>Like This One?</em></h2><p class="subtitle">Tell us what you want to build, '
               'your budget and timing, then pick a time for a free 30-minute call with our design manager.</p>'
               '<div class="gold-rule"></div></div><div class="lead-survey ls-dark" data-source="project-SLUG" '
               'data-tags="Website Survey, Project Page"></div></div></div>')

VIEWER_JS = r"""<script>
/* Project photo viewer: every #gallery .pj-shot opens here. Arrows, Escape, swipe, focus return. */
(function () {
  'use strict';
  var gal = document.getElementById('gallery');
  var shots = gal ? Array.prototype.slice.call(gal.querySelectorAll('.pj-shot')) : [];
  if (!shots.length) return;
  var slug = gal.getAttribute('data-project'), name = gal.getAttribute('data-name') || '';
  var lb = document.createElement('div');
  lb.className = 'pj-lb';
  lb.setAttribute('role', 'dialog');
  lb.setAttribute('aria-modal', 'true');
  lb.setAttribute('aria-label', name + ' photo viewer');
  lb.setAttribute('aria-hidden', 'true');
  lb.innerHTML =
    '<div class="pj-lb-top"><div class="pj-lb-title"></div><button type="button" class="pj-lb-x" aria-label="Close photo viewer">&times;</button></div>' +
    '<div class="pj-lb-stage"><button type="button" class="pj-lb-nav pj-lb-prev" aria-label="Previous photo">&larr;</button><img alt=""><button type="button" class="pj-lb-nav pj-lb-next" aria-label="Next photo">&rarr;</button></div>' +
    '<div class="pj-lb-bottom"><p class="pj-lb-meta" aria-live="polite"><span class="pj-lb-count"></span><span class="pj-lb-cap"></span></p><a href="#book" class="btn-gold pj-lb-book">Book a Design Call</a></div>';
  document.body.appendChild(lb);
  var title = lb.querySelector('.pj-lb-title'), stage = lb.querySelector('.pj-lb-stage'), img = stage.querySelector('img');
  var count = lb.querySelector('.pj-lb-count'), cap = lb.querySelector('.pj-lb-cap');
  var btnX = lb.querySelector('.pj-lb-x'), btnPrev = lb.querySelector('.pj-lb-prev'), btnNext = lb.querySelector('.pj-lb-next'), book = lb.querySelector('.pj-lb-book');
  title.textContent = name;
  var small = document.createElement('small'); small.textContent = 'Project gallery'; title.appendChild(small);
  var idx = 0, isOpen = false, lastFocus = null;

  function info(i) {
    var a = shots[i], im = a.querySelector('img');
    return { full: a.getAttribute('href'), src: im.getAttribute('src'), alt: im.getAttribute('alt') || '' };
  }
  function show(i) {
    idx = (i + shots.length) % shots.length;
    var want = idx, d = info(idx);
    img.src = d.src; img.alt = d.alt; img.classList.add('is-loading');
    count.textContent = (idx + 1) + ' / ' + shots.length;
    cap.textContent = d.alt;
    var hi = new Image();
    hi.onload = function () { if (want === idx && isOpen) { img.src = d.full; img.classList.remove('is-loading'); } };
    hi.onerror = function () { img.classList.remove('is-loading'); };
    hi.src = d.full;
    [idx + 1, idx - 1].forEach(function (j) { var n = new Image(); n.src = info((j + shots.length) % shots.length).src; });
  }
  function open(i) {
    lastFocus = document.activeElement;
    isOpen = true;
    show(i);
    lb.classList.add('open'); lb.setAttribute('aria-hidden', 'false');
    document.body.classList.add('gh-lock');
    btnX.focus({ preventScroll: true });
    try { gtag('event', 'project_photo_open', { project: slug, photo: idx + 1 }); } catch (e) {}
  }
  function close() {
    if (!isOpen) return;
    isOpen = false;
    lb.classList.remove('open'); lb.setAttribute('aria-hidden', 'true');
    document.body.classList.remove('gh-lock');
    if (lastFocus && lastFocus.focus) lastFocus.focus({ preventScroll: true });
  }
  function onClick(i) {
    return function (e) {
      if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || e.button > 0) return;
      e.preventDefault(); open(i);
    };
  }
  shots.forEach(function (a, i) { a.addEventListener('click', onClick(i)); });
  document.querySelectorAll('[data-open-photo]').forEach(function (a) {
    a.addEventListener('click', onClick(+a.getAttribute('data-open-photo') || 0));
  });
  btnX.addEventListener('click', close);
  btnPrev.addEventListener('click', function () { show(idx - 1); });
  btnNext.addEventListener('click', function () { show(idx + 1); });
  stage.addEventListener('click', function (e) { if (e.target === stage) close(); });
  book.addEventListener('click', function (e) {
    e.preventDefault();
    close();
    if (window.AriseDrawer) window.AriseDrawer.open('project-' + slug + '-viewer');
    else location.hash = 'book';
  });
  document.addEventListener('keydown', function (e) {
    if (!isOpen) return;
    if (e.key === 'Escape') { e.preventDefault(); close(); }
    else if (e.key === 'ArrowLeft') { e.preventDefault(); show(idx - 1); }
    else if (e.key === 'ArrowRight') { e.preventDefault(); show(idx + 1); }
    else if (e.key === 'Tab') {
      var f = [btnX, btnPrev, btnNext, book];
      var k = f.indexOf(document.activeElement);
      e.preventDefault();
      f[(k + (e.shiftKey ? -1 : 1) + f.length) % f.length].focus();
    }
  });
  var x0 = null;
  stage.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; }, { passive: true });
  stage.addEventListener('touchend', function (e) {
    if (x0 === null) return;
    var dx = e.changedTouches[0].clientX - x0; x0 = null;
    if (Math.abs(dx) > 40) show(idx + (dx < 0 ? 1 : -1));
  });
})();
</script>"""


# ── helpers ──
def esc(s):
    return html.escape(s, quote=True)


def url_of(path):
    return '/' + os.path.relpath(path, ROOT).replace(os.sep, '/')


def disk(u):
    return os.path.join(ROOT, u.split('#')[0].split('?')[0].lstrip('/'))


_sizes = {}


def img_size(path):
    """(width, height) from the JPEG frame header; falls back to `sips` if parsing fails."""
    if path in _sizes:
        return _sizes[path]
    wh = None
    try:
        with open(path, 'rb') as f:
            if f.read(2) == b'\xff\xd8':
                while True:
                    b = f.read(1)
                    while b and b != b'\xff':
                        b = f.read(1)
                    while b == b'\xff':
                        b = f.read(1)
                    if not b:
                        break
                    m = b[0]
                    if m == 0x01 or 0xD0 <= m <= 0xD8:
                        continue
                    seg = struct.unpack('>H', f.read(2))[0]
                    if m in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
                        f.read(1)
                        h, w = struct.unpack('>HH', f.read(4))
                        wh = (w, h)
                        break
                    f.seek(seg - 2, 1)
    except (OSError, struct.error):
        wh = None
    if not wh:
        out = subprocess.run(['sips', '-g', 'pixelWidth', '-g', 'pixelHeight', path], capture_output=True, text=True).stdout
        w = re.search(r'pixelWidth:\s*(\d+)', out)
        h = re.search(r'pixelHeight:\s*(\d+)', out)
        wh = (int(w.group(1)), int(h.group(1))) if w and h else (0, 0)
    _sizes[path] = wh
    return wh


def page_url(slug):
    return '%s/portfolio/%s' % (SITE, slug)


def ld(obj):
    return '<script type="application/ld+json">%s</script>' % json.dumps(obj, ensure_ascii=False).replace('</', '<\\/')


def eyebrow(text):
    return '<div class="eyebrow"><div class="eyebrow-line"></div><span class="eyebrow-text">%s</span><div class="eyebrow-line"></div></div>' % text


def h1_html(name):
    if name.startswith('The '):
        return 'The <em>%s</em>' % esc(name[4:])
    first, _, last = name.rpartition(' ')
    return '%s <em>%s</em>' % (esc(first), esc(last)) if first else '<em>%s</em>' % esc(name)


def page_title(p):
    base = '%s in %s, AZ' % (p['name'], p['city'])
    for suffix in (' | Arise Pools & Landscaping', ' | Arise Pools'):
        if len(base + suffix) <= 65:
            return base + suffix
    return None


def meta_description(p, n):
    b, c = p['blurb'].strip(), p['city']
    for tail in (' See all %d photos of this %s, AZ backyard by Arise Pools & Landscaping.' % (n, c),
                 ' See all %d photos of this %s, AZ backyard by Arise Pools.' % (n, c),
                 ' See all %d photos of this %s, AZ backyard.' % (n, c),
                 ' %d photos from %s, AZ, by Arise Pools.' % (n, c),
                 ' %d photos from %s, AZ.' % (n, c)):
        if 140 <= len(b + tail) <= 160:
            return b + tail
    return None


def blog_title(slug):
    f = os.path.join(ROOT, 'blog', slug + '.html')
    if not os.path.exists(f):
        return None
    m = re.search(r'<h1[^>]*>(.*?)</h1>', open(f, encoding='utf-8').read(), re.S)
    return html.unescape(re.sub(r'<[^>]+>', '', m.group(1))).strip() if m else None


def shared_blocks():
    """Pull the shared head and chrome markup out of index.html verbatim."""
    src = open(INDEX, encoding='utf-8').read()
    pats = {
        'gtag': r'<script async src="https://www\.googletagmanager\.com/gtag/js\?id=[^"]+"></script>\s*<script>.*?</script>',
        'styles': r'<link rel="preconnect" href="https://fonts\.googleapis\.com">.*?<link rel="stylesheet" href="/css/lead-survey\.css[^"]*">',
        'icons': r'<link rel="icon"[^>]*>\s*<link rel="apple-touch-icon"[^>]*>\s*<meta name="theme-color"[^>]*>',
        'chrome': r'<!-- Navigation -->.*?(?=\s*<!-- Hero Section -->)',
        'footer': r'<footer class="footer">.*?</footer>',
        'js_site': r'<script src="/js/site\.js[^"]*"></script>',
        'js_motion': r'<script src="/js/arise-motion\.js[^"]*"></script>',
        'js_survey': r'<script src="/js/lead-survey\.js[^"]*"></script>',
    }
    out, missing = {}, []
    for k, pat in pats.items():
        m = re.search(pat, src, re.S)
        if m:
            out[k] = m.group(0)
        else:
            missing.append(k)
    return out, missing


# ── page ──
def photo_rows(p):
    rows = []
    for ph in p['photos']:
        p900 = sync.photo_path(p, ph['n'], 900)
        p1800 = sync.photo_path(p, ph['n'], 1800)
        big = p1800 if os.path.exists(p1800) else p900
        w, h = img_size(p900)
        bw, bh = img_size(big)
        rows.append({'n': ph['n'], 'alt': ph['alt'].strip(), 'src': url_of(p900), 'w': w, 'h': h,
                     'big': url_of(big), 'bw': bw, 'bh': bh, 'has1800': big == p1800,
                     'full': sync.full_url(p, ph) or url_of(p900)})
    return rows


def story_photo(rows):
    """Tall photo for the editorial split: first portrait, else first non-cover photo close to 3:2, else the second."""
    rest = list(enumerate(rows))[1:] or list(enumerate(rows))
    for i, r in rest:
        if r['h'] > r['w']:
            return i, r
    for i, r in rest:
        if r['h'] >= 0.66 * r['w']:
            return i, r
    return rest[0]


def nearby_block(p):
    name, city = p['name'], p['city']
    if p.get('cityPage'):
        slug = p['cityPage'].rstrip('/').rsplit('/', 1)[-1]
        cities = [slug]
        where = 'in %s, AZ' % CITIES.get(slug, city)
        if slug == HQ_CITY:
            where += ', where Arise is headquartered'
        heading = 'Building in %s' % CITIES.get(slug, city)
        lead = '%s is %s. Planning a backyard nearby? Start with our %s page.' % (name, where, CITIES.get(slug, city))
    else:
        where, cities = NEARBY.get(p['cityFile'], ('in %s, AZ' % city, [HQ_CITY]))
        names = [CITIES[c] for c in cities]
        joined = ' and '.join(names)
        heading = 'Building Near %s' % joined
        lead = '%s is %s. The closest of our city pages are %s.' % (name, where, joined) if len(names) > 1 else \
            '%s is %s. The closest of our city pages is %s.' % (name, where, joined)
    links = ''.join('<a class="btn-ghost" href="/cities/%s">Pool Builder in %s</a>' % (c, esc(CITIES[c])) for c in cities)
    return heading, lead, cities, links


def build_page(p, live, shared, problems):
    slug, name, city = p['slug'], p['name'], p['city']
    rows = photo_rows(p)
    n = len(rows)
    url = page_url(slug)
    title = page_title(p)
    desc = meta_description(p, n)
    if not title:
        problems.append('%s: title is over 65 characters even with the short suffix' % slug)
        title = '%s in %s, AZ' % (name, city)
    if not desc:
        problems.append('%s: no meta description fits 140-160 characters (blurb is %d)' % (slug, len(p['blurb'])))
        desc = p['blurb']
    cover = next((r for r in rows if r['n'] == p.get('cover')), rows[0])
    if cover is not rows[0]:
        rows.remove(cover)
        rows.insert(0, cover)
    hero_img = cover['big']
    og_title = '%s in %s, AZ | Arise Pools & Landscaping' % (name, city)
    place = ', '.join(x for x in (p.get('neighborhood'), city) if x) + ', AZ'

    breadcrumb = {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': SITE + '/'},
        {'@type': 'ListItem', 'position': 2, 'name': 'Portfolio', 'item': SITE + '/portfolio'},
        {'@type': 'ListItem', 'position': 3, 'name': name, 'item': url}]}
    gallery = {'@context': 'https://schema.org', '@type': 'ImageGallery', '@id': url + '#gallery', 'name': name,
               'description': p['blurb'].strip(), 'url': url, 'inLanguage': 'en-US',
               'keywords': ', '.join(p.get('styles') or []),
               'contentLocation': {'@type': 'Place', 'name': place}, 'creator': BUSINESS,
               'image': [{'@type': 'ImageObject', 'contentUrl': SITE + r['big'], 'caption': r['alt'],
                          'width': r['bw'], 'height': r['bh']} for r in rows]}

    L = []
    a = L.append
    a('<!DOCTYPE html>')
    a('<html lang="en">')
    a('<head>')
    a(shared['gtag'])
    a('<meta charset="UTF-8">')
    a('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
    a('<title>%s</title>' % esc(title))
    a('<meta name="description" content="%s">' % esc(desc))
    a('<meta name="robots" content="index,follow,max-image-preview:large">')
    a(shared['styles'])
    a(PROJECT_CSS)
    a('<link rel="preload" as="image" href="%s">' % hero_img)
    a('<link rel="canonical" href="%s">' % url)
    a(shared['icons'])
    a('<meta property="og:site_name" content="Arise Pools &amp; Landscaping">')
    a('<meta property="og:type" content="article">')
    a('<meta property="og:title" content="%s">' % esc(og_title))
    a('<meta property="og:description" content="%s">' % esc(desc))
    a('<meta property="og:url" content="%s">' % url)
    a('<meta property="og:image" content="%s%s">' % (SITE, hero_img))
    a('<meta property="og:image:width" content="%d">' % cover['bw'])
    a('<meta property="og:image:height" content="%d">' % cover['bh'])
    a('<meta property="og:image:alt" content="%s">' % esc('%s, %s in %s, AZ' % (cover['alt'], name, city)))
    a('<meta name="twitter:card" content="summary_large_image">')
    a('<meta name="twitter:title" content="%s">' % esc(og_title))
    a('<meta name="twitter:description" content="%s">' % esc(desc))
    a('<meta name="twitter:image" content="%s%s">' % (SITE, hero_img))
    a('<meta name="twitter:image:alt" content="%s">' % esc('%s, %s in %s, AZ' % (cover['alt'], name, city)))
    a(ld(breadcrumb))
    a(ld(gallery))
    a('</head>')
    a('<body>')
    a(shared['chrome'])
    a('')
    a('<main id="main">')

    # Hero
    styles = p.get('styles') or []
    a('<div class="page-hero pj-hero" style="background-image:url(\'%s\');">' % hero_img)
    a('  <div class="page-hero-overlay"></div>')
    a('  <div class="page-hero-content">')
    a('    <nav aria-label="Breadcrumb"><ol class="gh-crumbs"><li><a href="/">Home</a></li><li><a href="/portfolio">Portfolio</a></li><li aria-current="page">%s</li></ol></nav>' % esc(name))
    a('    ' + eyebrow(esc(place)))
    a('    <h1>%s</h1>' % h1_html(name))
    a('    <p class="hero-subtitle">%s</p>' % esc(p['tagline']))
    a('    <div class="hero-ctas pj-hero-ctas">')
    a('      <a href="#book" class="btn-gold" data-book="project-%s">Book a Design Call</a>' % slug)
    a('      <a href="#gallery" class="btn-ghost">See the Photos</a>')
    a('    </div>')
    a('    <dl class="pj-facts">')
    a('      <div><dt>Location</dt><dd>%s</dd></div>' % esc(place))
    if styles:
        a('      <div><dt>Signature</dt><dd>%s</dd></div>' % ' &middot; '.join(esc(s[:1].upper() + s[1:]) for s in styles[:3]))
    a('      <div><dt>Photos</dt><dd>%d</dd></div>' % n)
    a('    </dl>')
    a('  </div>')
    a('</div>')
    a('')

    # Story
    si, sp = story_photo(rows)
    srcset = ' srcset="%s 900w, %s 1800w" sizes="(max-width: 960px) 100vw, 46vw"' % (sp['src'], sp['big']) if sp['has1800'] else ''
    a('<section class="section gh-sand" id="story" aria-labelledby="story-title">')
    a('  <div class="section-inner pj-story">')
    a('    <figure class="pj-story-media gh-clip-me">')
    a('      <a href="%s" data-open-photo="%d"><img src="%s"%s width="%d" height="%d" alt="%s" loading="lazy" decoding="async"></a>' % (
        esc(sp['full']), si, sp['src'], srcset, sp['w'], sp['h'], esc(sp['alt'])))
    a('      <figcaption>%s</figcaption>' % esc(sp['alt']))
    a('    </figure>')
    a('    <div class="pj-story-text">')
    a('      <div class="section-heading pj-left">')
    a('        ' + eyebrow('The Project'))
    a('        <h2 id="story-title">Inside <em>%s</em></h2>' % esc(name))
    a('        <div class="gold-rule"></div>')
    a('      </div>')
    a('      <p class="pj-lead">%s</p>' % esc(p['blurb'].strip()))
    for para in p.get('story') or []:
        a('      <p class="pj-p">%s</p>' % esc(para.strip()))
    if styles:
        a('      <ul class="pj-tags" aria-label="Design elements">%s</ul>' % ''.join('<li>%s</li>' % esc(s) for s in styles))
    a('    </div>')
    a('  </div>')
    a('</section>')
    a('')

    # Design details
    feats = p.get('features') or []
    if feats:
        a('<section class="section gh-sand-rev" id="details" aria-labelledby="details-title">')
        a('  <div class="section-inner">')
        a('    <div class="section-heading">')
        a('      ' + eyebrow('Design Details'))
        a('      <h2 id="details-title">What Makes It <em>Work</em></h2>')
        a('      <p class="subtitle">The decisions that shape %s, from the water to the edges of the lot.</p>' % esc(name))
        a('      <div class="gold-rule"></div>')
        a('    </div>')
        a('    <div class="pj-features">')
        for k, f in enumerate(feats, 1):
            a('      <article class="pj-feature gh-rv-me"><div class="pj-feature-num" aria-hidden="true">%02d</div><h3>%s</h3><p>%s</p></article>' % (
                k, esc(f['title'].strip()), esc(f['text'].strip())))
        a('    </div>')
        a('  </div>')
        a('</section>')
        a('')

    # Gallery
    a('<section class="section pj-gallery-sec" id="gallery" data-project="%s" data-name="%s" aria-labelledby="gallery-title">' % (slug, esc(name)))
    a('  <div class="section-wide">')
    a('    <div class="section-heading">')
    a('      ' + eyebrow('The Gallery'))
    a('      <h2 id="gallery-title">Walk the <em>Whole Project</em></h2>')
    a('      <p class="subtitle">%d photos from %s. Tap any photo to open it full size, then use the arrows to move through the set.</p>' % (n, esc(place)))
    a('      <div class="gold-rule"></div>')
    a('    </div>')
    a('    <div class="pj-masonry">')
    for r in rows:
        a('      <a class="pj-shot gh-rv-me" href="%s" style="--r:%.4f"><img src="%s" width="%d" height="%d" alt="%s" loading="lazy" decoding="async"></a>' % (
            esc(r['full']), r['w'] / float(r['h']), r['src'], r['w'], r['h'], esc(r['alt'])))
    a('    </div>')
    a('    <p class="gh-more"><a href="#book" class="btn-gold" data-book="project-%s-gallery">Book a Design Call</a></p>' % slug)
    a('  </div>')
    a('</section>')
    a('')

    # Services + nearby
    svcs = [s for s in (p.get('services') or []) if s in SERVICES]
    heading, lead, cities, links = nearby_block(p)
    a('<section class="section pj-dusk" id="services" aria-labelledby="services-title">')
    a('  <div class="section-inner pj-split">')
    a('    <div>')
    a('      <div class="section-heading pj-left">')
    a('        ' + eyebrow('What We Built'))
    a('        <h2 id="services-title">Services in <em>This Project</em></h2>')
    a('        <div class="gold-rule"></div>')
    a('      </div>')
    if svcs:
        a('      <ul class="pj-svc-list">')
        for k, s in enumerate(svcs, 1):
            nm, ds = SERVICES[s]
            a('        <li><a href="/services/%s"><span class="pj-svc-num">%02d</span><span><span class="pj-svc-name">%s</span><span class="pj-svc-desc">%s</span></span><span class="pj-svc-arrow" aria-hidden="true">&rarr;</span></a></li>' % (
                s, k, esc(nm), esc(ds)))
        a('      </ul>')
    else:
        a('      <p class="gh-more" style="text-align:left"><a href="/services" class="btn-ghost">See All Services</a></p>')
    a('    </div>')
    a('    <aside class="pj-near" aria-labelledby="near-title">')
    a('      ' + eyebrow('Nearby Service Area'))
    a('      <h3 id="near-title">%s</h3>' % esc(heading))
    a('      <p>%s</p>' % esc(lead))
    a('      <p class="pj-near-links">%s</p>' % links)
    posts = [(s, blog_title(s)) for s in (p.get('featuredInPosts') or [])]
    if posts:
        a('      <div class="pj-posts">')
        a('        <div class="pj-posts-label">Read the Story</div>')
        a('        <ul>%s</ul>' % ''.join('<li><a href="/blog/%s">%s</a></li>' % (s, esc(t or s)) for s, t in posts))
        a('      </div>')
    a('    </aside>')
    a('  </div>')
    a('</section>')
    a('')

    # More projects
    others = [q for q in live if q['slug'] != slug]
    if others:
        a('<section class="section pj-more-sec" id="more-projects" aria-labelledby="more-title">')
        a('  <div class="section-inner">')
        a('    <div class="section-heading">')
        a('      ' + eyebrow('More Signature Work'))
        a('      <h2 id="more-title">Keep <em>Exploring</em></h2>')
        a('      <div class="gold-rule"></div>')
        a('    </div>')
        a('    <div class="pj-more">')
        for q in others:
            cph = next((x for x in q['photos'] if x['n'] == q.get('cover')), q['photos'][0])
            cpath = sync.photo_path(q, cph['n'], 900)
            cw, chh = img_size(cpath)
            a('      <a class="pj-card gh-rv-me" href="/portfolio/%s"><div class="pj-card-media"><img src="%s" width="%d" height="%d" alt="%s" loading="lazy" decoding="async"></div><h3>%s</h3><div class="pj-card-meta">%s &middot; %s</div><span class="pj-card-link">View the project</span></a>' % (
                q['slug'], url_of(cpath), cw, chh, esc('%s, %s in %s, AZ' % (cph['alt'].strip(), q['name'], q['city'])),
                esc(q['name']), esc(q['city']), esc(q['tagline'])))
        a('    </div>')
        a('    <p class="gh-more"><a href="/portfolio" class="btn-ghost">View the Full Portfolio</a></p>')
        a('  </div>')
        a('</section>')
        a('')

    a(SURVEY_BAND.replace('SLUG', slug))
    a('</main>')
    a('')
    a(shared['footer'])
    a(shared['js_site'])
    a(shared['js_motion'])
    a(shared['js_survey'])
    a(VIEWER_JS)
    a('</body>')
    a('</html>')
    page = '\n'.join(L) + '\n'

    images = [{'loc': SITE + r['big'], 'caption': r['alt'], 'width': r['bw'], 'height': r['bh']} for r in rows]
    report = {'title': title, 'description': desc, 'photos': n, 'story_photo': sp['n'], 'cities': cities, 'services': svcs}
    return page, {'loc': url, 'title': title, 'images': images}, report


def validate(p, problems):
    slug = p['slug']
    for f in ('name', 'city', 'cityFile', 'tagline', 'blurb'):
        if not (p.get(f) or '').strip():
            problems.append('%s: missing %s' % (slug, f))
    if not p.get('photos'):
        problems.append('%s: live but has no photos' % slug)
        return False
    for ph in p['photos']:
        if not os.path.exists(sync.photo_path(p, ph['n'], 900)):
            problems.append('%s: missing %s' % (slug, os.path.relpath(sync.photo_path(p, ph['n'], 900), ROOT)))
        full = sync.full_url(p, ph)
        if full and not os.path.exists(disk(full)):
            problems.append('%s: missing full-size file %s' % (slug, full))
    for s in p.get('services') or []:
        if s not in SERVICES:
            problems.append('%s: unknown service slug %r' % (slug, s))
    if p.get('cityPage') and not os.path.exists(disk(p['cityPage'] + '.html')):
        problems.append('%s: cityPage %s has no file' % (slug, p['cityPage']))
    if not p.get('cityPage') and p['cityFile'] not in NEARBY:
        print('NOTE: %s has no cityPage and no NEARBY entry; linking the Gilbert page' % slug)
    for b in p.get('featuredInPosts') or []:
        if not blog_title(b):
            problems.append('%s: featured post blog/%s.html missing or has no <h1>' % (slug, b))
    for k in ('story', 'features'):
        if not p.get(k):
            print('NOTE: %s has no %s yet; the page renders without it' % (slug, k))
    text = json.dumps({k: p.get(k) for k in ('name', 'tagline', 'blurb', 'story', 'features')}, ensure_ascii=False)
    if EM_DASH in text:
        problems.append('%s: em-dash in registry copy' % slug)
    return not any(x.startswith(slug + ':') for x in problems)


def main():
    check_only = '--check' in sys.argv
    reg = json.load(open(REG, encoding='utf-8'))
    live = [p for p in reg['projects'] if p['status'] == 'live']
    problems = []
    shared, missing = shared_blocks()
    if missing:
        problems.append('index.html blocks not found: %s' % ', '.join(missing))
    for k, v in shared.items():
        if EM_DASH in v:
            problems.append('index.html %s block contains an em-dash' % k)
    if missing:
        print('PROBLEMS:\n  ' + '\n  '.join(problems))
        sys.exit(1)

    outputs, sitemap = {}, []
    for p in live:
        if not validate(p, problems):
            continue
        page, entry, rep = build_page(p, live, shared, problems)
        if EM_DASH in page:
            problems.append('%s: generated page contains an em-dash' % p['slug'])
        outputs[os.path.join(OUT_DIR, p['slug'] + '.html')] = page
        sitemap.append(entry)
        print('%-18s %2d chars title | %3d chars description | %2d photos | story photo %02d | cities %s' % (
            p['slug'], len(rep['title']), len(rep['description']), rep['photos'], rep['story_photo'], ','.join(rep['cities'])))
    outputs[SITEMAP_JSON] = json.dumps({
        '_readme': 'Generated by scripts/build-project-pages.py from data/projects.json; do not hand-edit. '
                   'One entry per project page: page URL and every image on it (absolute URL + caption) for the image sitemap.',
        'pages': sitemap}, indent=2, ensure_ascii=False) + '\n'

    live_slugs = {p['slug'] for p in live}
    if os.path.isdir(OUT_DIR):
        for f in sorted(os.listdir(OUT_DIR)):
            if f.endswith('.html') and f[:-5] not in live_slugs:
                print('NOTE: portfolio/%s is not a live project page (left in place)' % f)

    changed = [f for f, s in outputs.items() if not os.path.exists(f) or open(f, encoding='utf-8').read() != s]
    if check_only:
        for f in changed:
            problems.append('%s is out of date (run without --check)' % os.path.relpath(f, ROOT))
    else:
        os.makedirs(OUT_DIR, exist_ok=True)
        for f in changed:
            with open(f, 'w', encoding='utf-8') as fh:
                fh.write(outputs[f])
            print('wrote %s' % os.path.relpath(f, ROOT))
        if not changed:
            print('no changes')
    if problems:
        print('PROBLEMS:\n  ' + '\n  '.join(problems))
        sys.exit(1)
    print('OK (%d project pages)' % len(sitemap))


if __name__ == '__main__':
    main()
