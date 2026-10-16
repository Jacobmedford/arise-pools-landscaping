#!/usr/bin/env python3
"""Sync data/projects.json into the site.

- Regenerates the PROJECTS block in js/portfolio-gallery.js (between the BEGIN/END markers).
- Checks every live project's photo files exist (1800 + 900 widths).
- Reports live projects that have no data-project tile on portfolio.html.

Usage: python3 scripts/projects-sync.py [--check]   (--check = validate only, write nothing)
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REG = os.path.join(ROOT, 'data', 'projects.json')
GALLERY = os.path.join(ROOT, 'js', 'portfolio-gallery.js')
PORTFOLIO = os.path.join(ROOT, 'portfolio.html')
BEGIN = '  // BEGIN GENERATED PROJECTS'
END = '  // END GENERATED PROJECTS'


def photo_path(p, n, w):
    return os.path.join(ROOT, 'images', 'projects', p['slug'], '%s-%s-az-%02d-%d.jpg' % (p['slug'], p['cityFile'], n, w))


def full_url(p, ph):
    """Largest version for the lightbox: registry `full`, else a -full.jpg next to it, else the 1800px file."""
    if ph.get('full'):
        return ph['full']
    for suffix in ('full', 1800):
        rel = 'images/projects/%s/%s-%s-az-%02d-%s.jpg' % (p['slug'], p['slug'], p['cityFile'], ph['n'], suffix)
        if os.path.exists(os.path.join(ROOT, rel)):
            return '/' + rel
    return None


def js_str(s):
    return "'" + s.replace('\\', '\\\\').replace("'", "\\'") + "'"


def main():
    check_only = '--check' in sys.argv
    reg = json.load(open(REG))
    live = [p for p in reg['projects'] if p['status'] == 'live']
    problems = []

    slugs = [p['slug'] for p in reg['projects']]
    if len(slugs) != len(set(slugs)):
        problems.append('duplicate slugs in registry')
    for p in live:
        if not p['photos']:
            problems.append('%s: live but has no photos' % p['slug'])
        for ph in p['photos']:
            if not ph.get('alt') or ph['alt'].lower().startswith('photo '):
                problems.append('%s photo %s: needs a real alt text' % (p['slug'], ph['n']))
            if not os.path.exists(photo_path(p, ph['n'], 900)):
                problems.append('missing file %s' % os.path.relpath(photo_path(p, ph['n'], 900), ROOT))
            full = full_url(p, ph)
            if not full:
                problems.append('%s photo %s: no full-size or 1800px file' % (p['slug'], ph['n']))
            elif not os.path.exists(os.path.join(ROOT, full.lstrip('/'))):
                problems.append('missing full-size file %s' % full)
        if re.search(r'surname|client', p['name'], re.I):
            problems.append('%s: name looks like a placeholder' % p['slug'])

    lines = ['  var PROJECTS = {']
    for k, p in enumerate(live):
        photos = ', '.join('[%d, %s, %s]' % (ph['n'], js_str(ph['alt']), js_str(full_url(p, ph) or '')) for ph in p['photos'])
        lines.append("    %s: { name: %s, city: %s, img: P(%s, %s),\n      photos: [%s] }%s" % (
            js_str(p['slug']), js_str(p['name']), js_str(p['city']), js_str(p['slug']), js_str(p['cityFile']), photos,
            ',' if k < len(live) - 1 else ''))
    lines.append('  };')
    block = '\n'.join(lines) + '\n'

    src = open(GALLERY).read()
    i, j = src.find(BEGIN), src.find(END)
    if i < 0 or j < 0:
        problems.append('gallery markers not found in js/portfolio-gallery.js')
    else:
        start = src.index('\n', i) + 1
        new = src[:start] + block + src[j:]
        if not check_only and new != src:
            open(GALLERY, 'w').write(new)
            print('updated js/portfolio-gallery.js (%d live projects)' % len(live))

    tiles = set(re.findall(r'data-project="([^"]+)"', open(PORTFOLIO).read()))
    for p in live:
        if p['slug'] not in tiles:
            print('NOTE: %s is live but portfolio.html has no data-project tile for it' % p['slug'])

    pending = [p['name'] for p in reg['projects'] if p['status'] != 'live']
    print('live: %s' % ', '.join(p['name'] for p in live))
    print('awaiting photos: %s' % (', '.join(pending) or 'none'))
    if problems:
        print('PROBLEMS:\n  ' + '\n  '.join(problems))
        sys.exit(1)
    print('OK')


if __name__ == '__main__':
    main()
