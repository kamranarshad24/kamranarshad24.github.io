"""Duplicate-content safety audit across every language version."""
import json, os, re, sys, collections
import xml.etree.ElementTree as ET
sys.path.insert(0, os.path.dirname(__file__))
import i18n
ROOT, SITE = i18n.ROOT, i18n.SITE
langs = ["en"] + i18n.LIVE
fail = []
def path_of(lang, p):
    base = ROOT if lang == "en" else os.path.join(ROOT, lang)
    return os.path.join(base, (p + "index.html") if p == "" or p.endswith("/") else p)
titles = collections.defaultdict(list); descs = collections.defaultdict(list)
for lang in langs:
    for p in i18n.PAGES:
        s = open(path_of(lang, p), encoding="utf-8").read()
        cans = re.findall(r'<link rel="canonical" href="([^"]+)"', s)
        robots = re.search(r'<meta name="robots" content="([^"]+)"', s)
        if p in i18n.NOINDEX:
            if not robots or "noindex" not in robots.group(1): fail.append((lang, p, "thankyou not noindex"))
            continue
        if robots and "noindex" in robots.group(1): fail.append((lang, p, "unexpected noindex"))
        if cans != [i18n.page_url(lang, p)]: fail.append((lang, p, "canonical", cans))
        alts = dict(re.findall(r'<link rel="alternate" hreflang="([^"]+)" href="([^"]+)">', s))
        want = {l: i18n.page_url(l, p) for l in langs}; want["x-default"] = i18n.page_url("en", p)
        if alts != want: fail.append((lang, p, "hreflang", alts))
        if not re.search(r'<html lang="%s"' % lang, s): fail.append((lang, p, "html lang"))
        for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
            try: json.loads(m.group(1))
            except Exception as e: fail.append((lang, p, "bad json-ld", str(e)[:60]))
        t = re.search(r"<title>(.*?)</title>", s, re.S); d = re.search(r'<meta name="description" content="([^"]*)"', s)
        titles[t.group(1).strip()].append(lang + ":" + p)
        if d: descs[d.group(1)].append(lang + ":" + p)
        og = re.search(r'<meta property="og:url" content="([^"]+)"', s)
        if og and og.group(1) != i18n.page_url(lang, p): fail.append((lang, p, "og:url", og.group(1)))
dups_t = {k: v for k, v in titles.items() if len(v) > 1}
dups_d = {k: v for k, v in descs.items() if len(v) > 1}
# sitemap
ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9", "x": "http://www.w3.org/1999/xhtml"}
tree = ET.parse(os.path.join(ROOT, "sitemap.xml"))
urls = tree.getroot().findall("s:url", ns)
locs = [u.find("s:loc", ns).text for u in urls]
for u in urls:
    loc = u.find("s:loc", ns).text
    rel = loc[len(SITE):].lstrip("/")
    f = os.path.join(ROOT, rel + ("index.html" if rel == "" or rel.endswith("/") else ""))
    if not os.path.exists(f): fail.append(("sitemap", loc, "missing file"))
    if len(u.findall("x:link", ns)) != len(langs) + 1: fail.append(("sitemap", loc, "alt count"))
print("pages checked:", len(langs) * len(i18n.PAGES), "| sitemap urls:", len(locs), "unique:", len(set(locs)))
print("duplicate titles:", dups_t or "none"); print("duplicate descriptions:", dups_d or "none")
for f in fail: print("FAIL", f)
print("failures:", len(fail))
