#!/usr/bin/env python3
"""Append curated shots from a full shoot that already lives in the repo to a project's gallery.

Input is a curation JSON (written after viewing contact sheets):
  {"slug": "...", "sourceDir": "images-for-web-or-mls-3",
   "keep": [{"file": "50-web-or-mls-IMG_0764.jpg", "alt": "..."}, ...]}

For each kept file (in order) this makes the 900px thumbnail under
images/projects/<slug>/<slug>-<city>-az-NN-900.jpg and appends {n, alt, full} to
data/projects.json, where `full` points at the full-size original already in the repo
(the gallery lightbox serves it). Existing photos and their numbers are never touched.

Usage: python3 -I scripts/project-extend.py CURATION.json [--skip FILE ...]
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REG = os.path.join(ROOT, 'data', 'projects.json')


def main():
    from PIL import Image, ImageOps
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    cur = json.load(open(args[0]))
    skip = set(args[args.index('--skip') + 1:]) if '--skip' in args else set()
    reg = json.load(open(REG))
    p = next(x for x in reg['projects'] if x['slug'] == cur['slug'])
    out = os.path.join(ROOT, 'images', 'projects', p['slug'])
    os.makedirs(out, exist_ok=True)
    have_full = {ph.get('full') for ph in p['photos']}
    n = max([ph['n'] for ph in p['photos']] + [0])
    added = 0
    for k in cur['keep']:
        if k['file'] in skip:
            continue
        src_rel = '/%s/%s' % (cur['sourceDir'], k['file'])
        if src_rel in have_full:
            continue
        src = os.path.join(ROOT, cur['sourceDir'], k['file'])
        if not os.path.exists(src):
            sys.exit('missing source %s' % src)
        n += 1
        im = ImageOps.exif_transpose(Image.open(src)).convert('RGB')
        im.thumbnail((900, 1800), Image.LANCZOS)
        im.save(os.path.join(out, '%s-%s-az-%02d-900.jpg' % (p['slug'], p['cityFile'], n)), 'JPEG', quality=78, optimize=True, progressive=True)
        p['photos'].append(dict(n=n, alt=k['alt'], full=src_rel))
        added += 1
    json.dump(reg, open(REG, 'w'), indent=2, ensure_ascii=False)
    print('%s: added %d photos (now %d)' % (p['slug'], added, len(p['photos'])))


if __name__ == '__main__':
    main()
