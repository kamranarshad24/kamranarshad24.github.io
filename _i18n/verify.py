"""Checks a built language: tag balance vs English, internal links resolve, hreflang/canonical sane."""
import os, re, sys, collections
sys.path.insert(0, os.path.dirname(__file__))
import i18n
ROOT = i18n.ROOT
lang = sys.argv[1]
problems = []
def exists(path):
    from urllib.parse import unquote
    p = unquote(path.split("#")[0].split("?")[0])
    if p.endswith("/"): p += "index.html"
    return os.path.exists(os.path.join(ROOT, p.lstrip("/")))
for p in i18n.PAGES:
    en = open(i18n.src_file(p), encoding="utf-8").read()
    fn = os.path.join(ROOT, lang, (p + "index.html") if p == "" or p.endswith("/") else p)
    tr = open(fn, encoding="utf-8").read()
    strip = lambda s: re.sub(r'<script\b.*?</script>|<details class="lang-sw">.*?</details>|<link rel="alternate"[^>]*>', "", s, flags=re.S)
    ce = collections.Counter(t.lower() for t in re.findall(r"</?([a-zA-Z0-9]+)", strip(en)))
    ct = collections.Counter(t.lower() for t in re.findall(r"</?([a-zA-Z0-9]+)", strip(tr)))
    if ce != ct:
        diff = {k: (ce[k], ct[k]) for k in set(ce) | set(ct) if ce[k] != ct[k]}
        problems.append((p, "tag counts differ", diff))
    for m in re.finditer(r'\b(?:href|src|action|poster|data-img|data-pdf)="([^"]+)"|\bsrcset="([^" ]+)', tr):
        u = m.group(1) or m.group(2)
        if u.startswith(("http", "mailto:", "tel:", "#", "javascript:", "data:", "//")):
            if u.startswith(i18n.SITE) and not exists(u[len(i18n.SITE):] or "/"): problems.append((p, "dead abs link", u))
            continue
        if not u.startswith("/"): problems.append((p, "relative url", u)); continue
        if not exists(u): problems.append((p, "dead link", u))
    if p not in i18n.NOINDEX:
        can = re.search(r'<link rel="canonical" href="([^"]+)"', tr).group(1)
        if can != i18n.page_url(lang, p): problems.append((p, "canonical", can))
        hl = re.findall(r'hreflang="([^"]+)" href="([^"]+)"', tr)
        if len(hl) != len(i18n.LIVE) + 2: problems.append((p, "hreflang count", len(hl)))
    if f'<html lang="{lang}"' not in tr: problems.append((p, "html lang"))
for x in problems: print(x)
print(lang, "problems:", len(problems))
