#!/usr/bin/env python3
"""Page-speed pass for images in the HTML (macOS: uses `sips`).

- <img> pointing at a heavy original (over 250 KB or wider than 1200px) is switched to a 900px
  copy in images/opt/ (made once, quality 72).
- Inline background-image heroes on a heavy original are switched to an 1800px copy.
- Every <img> gets real width/height (stops layout shift), and every <img> outside the nav and
  heroes gets loading="lazy" decoding="async".
Meta tags and JSON-LD keep their original absolute URLs.

Usage: python3 scripts/optimize-images.py [--check] [file.html ...]   (default: every page)
"""
import os, re, shutil, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OPT = os.path.join(ROOT, 'images', 'opt')
SKIP_DIRS = {'node_modules', 'qa', 'scripts', 'ops', 'data', 'preview-assets', 'wix-velo-backend', 'wix-velo-frontend', 'images', 'css', 'js'}
HEAVY_BYTES, HEAVY_W = 250 * 1024, 1200
_dims = {}


def dims(rel):
    if rel not in _dims:
        out = subprocess.run(['sips', '-g', 'pixelWidth', '-g', 'pixelHeight', os.path.join(ROOT, rel)], capture_output=True, text=True).stdout
        w = re.search(r'pixelWidth: (\d+)', out); h = re.search(r'pixelHeight: (\d+)', out)
        _dims[rel] = (int(w.group(1)), int(h.group(1))) if w and h else None
    return _dims[rel]


def derivative(src, width, check):
    rel = src.lstrip('/')
    path = os.path.join(ROOT, rel)
    if not os.path.exists(path) or rel.startswith(('images/opt/', 'images/projects/')):
        return src  # project photos are already web-sized by the intake pipeline
    d = dims(rel)
    if not d or (os.path.getsize(path) <= HEAVY_BYTES and d[0] <= HEAVY_W):
        return src
    if d[0] <= width and os.path.getsize(path) <= HEAVY_BYTES:
        return src
    tag = rel.split('/')[0].replace('images-for-web-or-mls', 'mls').replace('images', 'img')
    stem = os.path.splitext(os.path.basename(rel))[0]
    out_rel = 'images/opt/%s-%s-%d.jpg' % (tag, stem, width)
    out = os.path.join(ROOT, out_rel)
    if os.path.exists(out):
        return '/' + out_rel
    if check:
        return src
    os.makedirs(OPT, exist_ok=True)
    tmp = os.path.join(tempfile.gettempdir(), os.path.basename(out))
    args = ['sips', '-s', 'format', 'jpeg', '-s', 'formatOptions', '72']
    if d[0] > width:
        args += ['--resampleWidth', str(width)]
    subprocess.run(args + [path, '--out', tmp], capture_output=True, check=True)
    if os.path.getsize(tmp) > 0.85 * os.path.getsize(path):
        os.remove(tmp)
        return src  # re-encoding did not pay off; keep the original
    shutil.move(tmp, out)
    return '/' + out_rel


def fix_img(tag, in_nav, check):
    m = re.search(r'\ssrc="([^"]+)"', tag)
    if not m or not m.group(1).startswith('/'):
        return tag
    src = derivative(m.group(1), 900, check)
    tag = tag.replace(m.group(0), ' src="%s"' % src)
    d = dims(src.lstrip('/')) if os.path.exists(os.path.join(ROOT, src.lstrip('/'))) else None
    if d and 'width=' not in tag:
        tag = re.sub(r'\s*/?>$', lambda e: ' width="%d" height="%d"%s' % (d[0], d[1], e.group(0)), tag)
    if not in_nav and 'loading=' not in tag and 'fetchpriority' not in tag:
        tag = re.sub(r'\s*/?>$', lambda e: ' loading="lazy" decoding="async"%s' % e.group(0), tag)
    return tag


def process(rel, check):
    path = os.path.join(ROOT, rel)
    html = open(path, encoding='utf-8').read()
    head, sep, body = html.partition('</head>')
    if not sep:
        return 0
    # heroes: inline background images
    body2 = re.sub(r"(background-image:\s*url\(['\"]?)(/[^'\")]+\.jpe?g)(['\"]?\))",
                   lambda m: m.group(1) + derivative(m.group(2), 1800, check) + m.group(3), body)
    # imgs, tracking whether we are inside <nav> or a hero block
    out, pos = [], 0
    for m in re.finditer(r'<img\b[^>]*>', body2):
        before = body2[:m.start()]
        in_nav = before.rfind('<nav') > before.rfind('</nav>')
        out.append(body2[pos:m.start()]); out.append(fix_img(m.group(0), in_nav, check)); pos = m.end()
    out.append(body2[pos:])
    new = head + sep + ''.join(out)
    if new != html and not check:
        open(path, 'w', encoding='utf-8').write(new)
    return int(new != html)


def main():
    check = '--check' in sys.argv
    files = [a for a in sys.argv[1:] if a.endswith('.html')]
    if not files:
        for dp, dn, fn in os.walk(ROOT):
            dn[:] = [d for d in dn if d not in SKIP_DIRS and not d.startswith('.')]
            files += [os.path.relpath(os.path.join(dp, f), ROOT) for f in fn if f.endswith('.html') and not f.startswith('_')]
    changed = sum(process(f, check) for f in sorted(files))
    print('%d of %d pages %s' % (changed, len(files), 'would change' if check else 'changed'))


if __name__ == '__main__':
    main()
