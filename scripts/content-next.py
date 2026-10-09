#!/usr/bin/env python3
"""Decide the next Arise blog target, deterministically.

  python3 scripts/content-next.py                 -> print the next target as JSON (changes nothing)
  python3 scripts/content-next.py --record SLUG   -> after a post is LIVE: advance the rotation,
                                                     log it, and add SLUG to the featured project's featuredInPosts

Focus alternates city -> neighborhood. Cities rotate in data/content-rotation.json order; each city
walks through its neighborhoods. Featured project = a live project in the same city if one exists,
otherwise the live project featured least (registry order breaks ties).
"""
import json, os, sys, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROT = os.path.join(ROOT, 'data', 'content-rotation.json')
REG = os.path.join(ROOT, 'data', 'projects.json')


def decide(rot, reg):
    st = rot['state']
    city = rot['cities'][st['nextCityIndex'] % len(rot['cities'])]
    focus = st['nextFocus']
    hood = None
    if focus == 'neighborhood' and city['neighborhoods']:
        hood = city['neighborhoods'][st['neighborhoodCursor'].get(city['slug'], 0) % len(city['neighborhoods'])]
    live = [p for p in reg['projects'] if p['status'] == 'live']
    same = [p for p in live if p['city'].lower() == city['name'].lower()]
    pool = same or live
    feat = min(pool, key=lambda p: (len(p['featuredInPosts']), live.index(p))) if pool else None
    return dict(focus=focus, city=city['name'], citySlug=city['slug'], cityPage=city['page'], neighborhood=hood,
                featuredProject=feat and dict(slug=feat['slug'], name=feat['name'], city=feat['city'],
                                              galleryLink='/portfolio#' + feat['slug'], sameCity=bool(same)),
                keywordHint=('custom pool builder %s AZ' % (hood or city['name'])) if focus == 'city' or hood else None)


def main():
    rot, reg = json.load(open(ROT)), json.load(open(REG))
    d = decide(rot, reg)
    if '--record' not in sys.argv:
        print(json.dumps(d, indent=2)); return
    slug = sys.argv[sys.argv.index('--record') + 1]
    st = rot['state']
    rot['history'].append(dict(date=datetime.date.today().isoformat(), post=slug, focus=d['focus'], city=d['city'],
                               neighborhood=d['neighborhood'], featuredProject=d['featuredProject'] and d['featuredProject']['slug']))
    if d['focus'] == 'neighborhood':
        st['neighborhoodCursor'][d['citySlug']] = st['neighborhoodCursor'].get(d['citySlug'], 0) + 1
        st['nextCityIndex'] = (st['nextCityIndex'] + 1) % len(rot['cities'])
        st['nextFocus'] = 'city'
    else:
        st['nextFocus'] = 'neighborhood'
    if d['featuredProject']:
        p = next(p for p in reg['projects'] if p['slug'] == d['featuredProject']['slug'])
        if slug not in p['featuredInPosts']: p['featuredInPosts'].append(slug)
        json.dump(reg, open(REG, 'w'), indent=2, ensure_ascii=False)
    json.dump(rot, open(ROT, 'w'), indent=2)
    print('recorded %s; next focus %s, next city %s' % (slug, st['nextFocus'], rot['cities'][st['nextCityIndex']]['name']))


if __name__ == '__main__':
    main()
