#!/usr/bin/env python3
"""Add (or fill in) a project from a folder of raw photos.

Optimizes every .jpg/.jpeg/.png in --src into 1800px and 900px progressive JPEGs at
images/projects/<slug>/<slug>-<cityFile>-az-NN-<w>.jpg, writes a contact sheet for
reviewing the shots, and adds/updates the project in data/projects.json with
placeholder alt text ("Photo N") that MUST be replaced before syncing.

The project name is the creative name (see ops/CONTENT-AGENT.md, Naming Function).
Never a client surname.

Usage:
  python3 -I scripts/project-intake.py --src DIR --slug the-desert-escape \
      --name "The Desert Escape" --city "Superstition Mountains" [--tagline "Luxury Outdoor Living"] [--neighborhood X]
"""
import argparse, glob, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REG = os.path.join(ROOT, 'data', 'projects.json')


def city_file(city):
    return re.sub(r'[^a-z0-9]+', '-', city.lower()).strip('-')


def main():
    from PIL import Image, ImageOps, ImageDraw
    Image.MAX_IMAGE_PIXELS = None
    ap = argparse.ArgumentParser()
    ap.add_argument('--src', required=True)
    ap.add_argument('--slug', required=True)
    ap.add_argument('--name', required=True)
    ap.add_argument('--city', required=True)
    ap.add_argument('--tagline', default='')
    ap.add_argument('--neighborhood', default=None)
    ap.add_argument('--sheet-dir', default=os.environ.get('TMPDIR', '/tmp'))
    a = ap.parse_args()

    if not re.fullmatch(r'[a-z0-9]+(-[a-z0-9]+)*', a.slug):
        sys.exit('slug must be lowercase-hyphenated, e.g. the-desert-escape')
    cf = city_file(a.city)
    files = sorted(f for f in glob.glob(os.path.join(a.src, '*')) if f.lower().endswith(('.jpg', '.jpeg', '.png')))
    if not files:
        sys.exit('no images in %s' % a.src)
    out = os.path.join(ROOT, 'images', 'projects', a.slug)
    os.makedirs(out, exist_ok=True)

    thumbs = []
    for i, f in enumerate(files, 1):
        im = ImageOps.exif_transpose(Image.open(f)).convert('RGB')
        for w in (1800, 900):
            r = im.copy()
            r.thumbnail((w, w * 2), Image.LANCZOS)
            r.save(os.path.join(out, '%s-%s-az-%02d-%d.jpg' % (a.slug, cf, i, w)), 'JPEG', quality=78, optimize=True, progressive=True)
        t = im.copy(); t.thumbnail((360, 360)); thumbs.append((t, '%02d %s' % (i, os.path.basename(f))))

    cols, cw, ch = 4, 360, 260
    sheet = Image.new('RGB', (cols * cw, ((len(thumbs) + cols - 1) // cols) * ch), 'white')
    d = ImageDraw.Draw(sheet)
    for k, (t, lab) in enumerate(thumbs):
        x, y = (k % cols) * cw, (k // cols) * ch
        sheet.paste(t, (x, y)); d.text((x + 4, y + ch - 18), lab, fill='black')
    sheet_path = os.path.join(a.sheet_dir, 'arise-sheet-%s.jpg' % a.slug)
    sheet.save(sheet_path, quality=70)

    reg = json.load(open(REG))
    proj = next((p for p in reg['projects'] if p['slug'] == a.slug), None)
    if proj is None:
        proj = dict(slug=a.slug, status='awaiting-photos', name=a.name, city=a.city, neighborhood=a.neighborhood, cityFile=cf,
                    cityPage=None, tagline=a.tagline, styles=[], blurb='', photos=[], cover=None, featuredInPosts=[])
        reg['projects'].append(proj)
    proj.update(name=a.name, city=a.city, cityFile=cf)
    if a.tagline: proj['tagline'] = a.tagline
    if a.neighborhood: proj['neighborhood'] = a.neighborhood
    if os.path.exists(os.path.join(ROOT, 'cities', cf + '.html')):
        proj['cityPage'] = '/cities/' + cf
    proj['photos'] = [dict(n=i, alt='Photo %d' % i) for i in range(1, len(files) + 1)]
    proj['cover'] = 1
    json.dump(reg, open(REG, 'w'), indent=2, ensure_ascii=False)

    print('optimized %d photos -> images/projects/%s/' % (len(files), a.slug))
    print('contact sheet: %s' % sheet_path)
    print('NEXT: view the sheet, write real alt text + order + cover + styles + blurb in data/projects.json,')
    print('      set status "live", add a portfolio tile with data-project="%s", then run scripts/projects-sync.py' % a.slug)


if __name__ == '__main__':
    main()
