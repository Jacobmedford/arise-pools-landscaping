#!/usr/bin/env python3
"""Ping IndexNow (Bing, Yandex, Seznam, Naver) with every URL in sitemap.xml, or the URLs given.

The key file lives at the site root (<key>.txt); this script finds it automatically.
Google does not use IndexNow: Google discovers changes through sitemap.xml and Search Console.

Usage: python3 scripts/indexnow.py                 (all sitemap URLs)
       python3 scripts/indexnow.py URL [URL ...]   (only these, e.g. a new blog post)
Run it only after the change is live on www.arisepal.com.
"""
import glob, json, os, re, sys, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOST = 'www.arisepal.com'


def main():
    keys = [os.path.basename(p)[:-4] for p in glob.glob(os.path.join(ROOT, '*.txt'))
            if re.fullmatch(r'[0-9a-f]{32}', os.path.basename(p)[:-4])]
    if len(keys) != 1:
        sys.exit('expected exactly one IndexNow key file at the repo root, found %d' % len(keys))
    key = keys[0]
    urls = sys.argv[1:] or re.findall(r'<loc>([^<]+)</loc>', open(os.path.join(ROOT, 'sitemap.xml')).read())
    body = json.dumps({'host': HOST, 'key': key, 'keyLocation': 'https://%s/%s.txt' % (HOST, key), 'urlList': urls}).encode()
    req = urllib.request.Request('https://api.indexnow.org/indexnow', data=body,
                                 headers={'Content-Type': 'application/json; charset=utf-8'})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            print('IndexNow', r.status, 'for', len(urls), 'urls')
    except urllib.error.HTTPError as e:
        sys.exit('IndexNow %s: %s' % (e.code, e.read()[:300]))


if __name__ == '__main__':
    main()
