#!/usr/bin/env python3
"""Regenerate sitemap.xml from the HTML files in the repo.

- One <url> per indexable page (skips noindex pages, pages whose canonical points elsewhere,
  and repo files that are not deployed).
- <lastmod> = last git commit date of the file, or today if it has uncommitted changes.
- Image sitemap entries for every project photo and inline image on the page, so Google Images
  can index the galleries.
- Also writes section sitemaps (sitemap-blog.xml, sitemap-funnels.xml) so Search Console can
  report indexing for the blog and the lead funnels on their own. sitemap.xml stays the full list.

Usage: python3 scripts/build-sitemap.py [--check]   (--check = print the summary, write nothing)
Run it after adding or changing pages (the blog routine runs it after each new post).
"""
import datetime, os, re, subprocess, sys
from xml.sax.saxutils import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://www.arisepal.com'
OUT = os.path.join(ROOT, 'sitemap.xml')
SKIP_DIRS = {'node_modules', 'qa', 'scripts', 'ops', 'data', 'preview-assets', 'wix-velo-backend',
             'wix-velo-frontend', '.git', '.vercel', 'images', 'css', 'js'}
SKIP_FILES = {'Arise-Dream-Center-Configurator.html', 'Arise-Pools-Visual-Preview.html', '_home-body.html'}
IMG_RE = re.compile(r'''(?:src=|url\(\s*['"]?)["']?(/images[^"')\s]+\.(?:jpe?g|png|webp))''', re.I)
TODAY = datetime.date.today().isoformat()
FUNNELS = {'/oasis', '/configurator', '/guide', '/contact'}
SECTIONS = {
    'sitemap-blog.xml': lambda path: path == '/blog' or path.startswith('/blog/'),
    'sitemap-funnels.xml': lambda path: path in FUNNELS,
}


def git_date(rel):
    dirty = subprocess.run(['git', 'status', '--porcelain', '--', rel], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    if dirty:
        return TODAY
    out = subprocess.run(['git', 'log', '-1', '--format=%cs', '--', rel], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    return out or TODAY


def url_for(rel):
    path = rel[:-5]
    if path == 'index':
        return SITE + '/'
    if path.endswith('/index'):
        path = path[:-6]
    return SITE + '/' + path


def pages():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS and not d.startswith('.'))
        for f in sorted(filenames):
            if f.endswith('.html') and f not in SKIP_FILES and not f.startswith('_'):
                yield os.path.relpath(os.path.join(dirpath, f), ROOT)


def main():
    entries, skipped = [], []
    for rel in pages():
        html = open(os.path.join(ROOT, rel), encoding='utf-8').read()
        robots = re.search(r'<meta[^>]+name=["\']robots["\'][^>]*content=["\']([^"\']+)', html, re.I)
        if robots and 'noindex' in robots.group(1).lower():
            skipped.append((rel, 'noindex')); continue
        url = url_for(rel)
        canon = re.search(r'<link[^>]+rel=["\']canonical["\'][^>]*href=["\']([^"\']+)', html, re.I)
        if canon and canon.group(1).rstrip('/') != url.rstrip('/'):
            skipped.append((rel, 'canonical -> ' + canon.group(1))); continue
        imgs = []
        for m in IMG_RE.finditer(html):
            u = SITE + m.group(1)
            if u not in imgs and os.path.exists(os.path.join(ROOT, m.group(1).lstrip('/'))):
                imgs.append(u)
        entries.append((url, git_date(rel), imgs[:1000]))
    entries.sort(key=lambda e: (e[0] != SITE + '/', e[0]))

    def render(rows):
        lines = ['<?xml version="1.0" encoding="UTF-8"?>',
                 '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">']
        for url, lastmod, imgs in rows:
            lines.append('  <url>')
            lines.append('    <loc>%s</loc>' % escape(url))
            lines.append('    <lastmod>%s</lastmod>' % lastmod)
            for u in imgs:
                lines.append('    <image:image><image:loc>%s</image:loc></image:image>' % escape(u))
            lines.append('  </url>')
        lines.append('</urlset>')
        return '\n'.join(lines) + '\n'
    lines = render(entries)
    section_rows = {name: [e for e in entries if test(e[0][len(SITE):] or '/')] for name, test in SECTIONS.items()}

    print('%d urls, %d images, %d skipped' % (len(entries), sum(len(e[2]) for e in entries), len(skipped)))
    for rel, why in skipped:
        print('  skip %s (%s)' % (rel, why))
    for name, rows in section_rows.items():
        print('  %s: %d urls' % (name, len(rows)))
    if '--check' not in sys.argv:
        open(OUT, 'w', encoding='utf-8').write(lines)
        print('wrote', os.path.relpath(OUT, ROOT))
        for name, rows in section_rows.items():
            open(os.path.join(ROOT, name), 'w', encoding='utf-8').write(render(rows))
            print('wrote', name)


if __name__ == '__main__':
    main()
