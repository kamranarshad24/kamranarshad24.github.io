"""Multilingual build for marketingkamran.com.

  python _i18n/i18n.py extract          -> _i18n/segments.json (every translatable string)
  python _i18n/i18n.py missing de       -> _i18n/todo-de.json (segments with no translation yet)
  python _i18n/i18n.py build            -> /<lang>/ pages, hreflang on all pages, sitemap.xml

English pages stay the source of truth. Translations live in _i18n/<lang>.json as
{segment_id: translated_text}. Jekyll does not publish folders starting with "_".
"""
import hashlib, html, json, os, re, sys
from urllib.parse import urljoin, urlsplit

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HERE = os.path.join(ROOT, "_i18n")
SITE = "https://marketingkamran.com"

LANGS = {  # code: (native name, og:locale, markets for schema areaServed)
    "de": ("Deutsch", "de_DE", ["Germany", "Austria", "Switzerland"]),
    "fr": ("Français", "fr_FR", ["France", "Belgium", "Switzerland", "Canada"]),
    "es": ("Español", "es_ES", ["Spain", "Mexico", "Colombia", "Argentina", "Chile"]),
    "it": ("Italiano", "it_IT", ["Italy", "Switzerland"]),
    "nl": ("Nederlands", "nl_NL", ["Netherlands", "Belgium"]),
    "pt": ("Português", "pt_BR", ["Brazil", "Portugal"]),
}
LIVE = [c for c in LANGS if os.path.exists(os.path.join(HERE, c + ".json"))]

PAGES = [  # English path relative to site root ("" = homepage)
    "", "google-ads-management.html", "meta-ads-management.html", "ecommerce-ppc-management.html",
    "local-seo-services.html", "conversion-tracking-setup.html", "white-label-ppc-for-agencies.html",
    "alphamart.html", "the-body-essential.html", "smile-line-dental.html", "mr-expert-carpet-cleaning.html",
    "brizaa.html", "wispr-flow-clone.html", "ai-content-builder.html", "privacy-policy.html",
    "blog/", "blog/capi-duplicate-purchase-events-deduplication.html",
    "blog/google-ads-account-audit-lead-generation.html", "blog/google-ads-call-tracking-local-business.html",
    "blog/google-ads-conversion-tracking-not-working.html", "blog/google-ads-offline-conversions-booked-jobs.html",
    "blog/local-seo-service-pages-service-business.html", "blog/meta-ads-account-audit-inherited.html",
    "blog/meta-ads-more-sales-than-shopify.html", "blog/meta-pixel-not-tracking-purchases-shopify.html",
    "blog/meta-pixel-reporting-fake-purchases.html", "blog/scaling-meta-campaigns-bad-data.html",
    "blog/shopify-additional-scripts-deadline-tracking.html", "blog/snapchat-purchase-event-not-firing.html",
    "blog/two-meta-pixels-shopify-problem.html", "thankyou.html",
]
NOINDEX = {"thankyou.html"}
PAGE_SET = set(PAGES) | {"index.html", "blog/index.html"}

def src_file(p):
    return os.path.join(ROOT, (p + "index.html") if p == "" or p.endswith("/") else p)

INLINE = {"a", "strong", "b", "em", "i", "span", "br", "code", "sup", "sub", "small", "mark",
          "abbr", "time", "u", "s", "kbd", "tspan", "wbr"}
VOID = {"br", "wbr", "img", "input", "meta", "link", "hr", "source"}
TOKEN = re.compile(r"<!--.*?-->|<(script|style|pre|textarea|svg:style)\b.*?</\1\s*>|<[^>]+>|[^<]+", re.S | re.I)
ATTRS = ("alt", "title", "aria-label", "placeholder", "data-title", "data-video-title")
META_KEYS = ("description", "og:title", "og:description", "twitter:title", "twitter:description", "og:image:alt")
LD_KEYS = {"name", "description", "headline", "text", "serviceType", "jobTitle", "alternativeHeadline",
           "abstract", "caption", "articleSection", "keywords", "about", "disambiguatingDescription"}
KEEP = {"Kamran Arshad", "Kamran", "Arshad", "Marketing Kamran"}

def sid(text):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:12]

def norm(s):
    return re.sub(r"\s+", " ", s).strip()

def has_words(s):
    t = re.sub(r"<[^>]+>|&[a-z#0-9]+;", " ", s)
    return re.search(r"[A-Za-z]{2,}", t) is not None and norm(t) not in KEEP

def tag_name(tok):
    m = re.match(r"</?\s*([a-zA-Z0-9:-]+)", tok)
    return m.group(1).lower() if m else ""

# ---- inline placeholders: <a href=..>x</a> becomes <t0>x</t0> so translations never touch markup
def to_placeholders(fragment):
    tags, out, stack = [], [], []
    for m in re.finditer(r"<[^>]+>|[^<]+", fragment):
        tok = m.group(0)
        if not tok.startswith("<"):
            out.append(tok); continue
        name = tag_name(tok)
        if tok.startswith("</") and stack:
            out.append("</t%d>" % stack.pop())
        elif tok.startswith("</"):  # closes a tag opened before this segment
            tags.append(tok); out.append("<t%d/>" % (len(tags) - 1))
        elif name in VOID or tok.endswith("/>"):
            tags.append(tok); out.append("<t%d/>" % (len(tags) - 1))
        else:
            tags.append(tok); stack.append(len(tags) - 1); out.append("<t%d>" % (len(tags) - 1))
    return norm("".join(out)), tags

def from_placeholders(text, tags, ph):
    want = sorted(re.findall(r"</?t\d+/?>", ph))
    if sorted(re.findall(r"</?t\d+/?>", text)) != want:
        raise ValueError("placeholder mismatch:\n  en: %s\n  tr: %s" % (ph, text))
    def rep(m):
        close, i, void = m.group(1), int(m.group(2)), m.group(3)
        if i >= len(tags):
            raise ValueError("bad placeholder t%d in: %s" % (i, text))
        if close:
            return "</%s>" % tag_name(tags[i])
        if void and tags[i].startswith("</"):
            return tags[i]
        return tags[i]
    return re.sub(r"<(/?)t(\d+)(/?)>", rep, text)

# ---- page walker: yields ("text", start, end, fragment) and ("attr", ...) etc.
def walk(src):
    """Return list of edits: (start, end, kind, payload). kind: seg|attr|ld."""
    edits, buf, buf_start = [], [], None
    def flush(end):
        nonlocal buf, buf_start
        if buf:
            frag = "".join(buf)
            lead = re.match(r"\s*", frag).group(0)
            trail = re.search(r"\s*$", frag).group(0)
            core = frag[len(lead):len(frag) - len(trail)] if trail else frag[len(lead):]
            # a fragment that is only tags (e.g. <br>) or has no words is left alone
            if core and has_words(core):
                # strip wrapping tags that open at start and close at end only if balanced: keep as-is
                edits.append((buf_start + len(lead), end - len(trail), "seg", core))
        buf, buf_start = [], None
    for m in TOKEN.finditer(src):
        tok, s, e = m.group(0), m.start(), m.end()
        if tok.startswith("<!--"):
            continue
        if tok.startswith("<"):
            name = tag_name(tok)
            low = tok[:80].lower()
            if low.startswith("<script") and "ld+json" in low:
                flush(s); edits.append((s, e, "ld", tok)); continue
            if low.startswith(("<script", "<style", "<pre", "<textarea")):
                flush(s); continue
            for a in ATTRS + ("content", "value"):
                for am in re.finditer(r'\s%s="([^"]*)"' % re.escape(a), tok):
                    val = am.group(1)
                    if a == "content":
                        nm = re.search(r'(?:name|property)="([^"]+)"', tok)
                        if not (name == "meta" and nm and nm.group(1) in META_KEYS):
                            continue
                    if a == "value":
                        tp = re.search(r'type="([^"]+)"', tok)
                        nm = re.search(r'name="([^"]+)"', tok)
                        if not (tp and tp.group(1) in ("submit", "button")):
                            continue
                    if has_words(val):
                        edits.append((s + am.start(1), s + am.end(1), "attr", val))
            if name in INLINE:
                if buf_start is None and (tok.startswith("</") or name in VOID):
                    continue
                if buf_start is None: buf_start = s
                buf.append(tok)
            else:
                flush(s)
        else:
            if buf_start is None: buf_start = s
            buf.append(tok)
    flush(len(src))
    segs = [(s, e) for s, e, k, _ in edits if k == "seg"]
    edits = [x for x in edits if x[2] != "attr" or not any(a <= x[0] and x[1] <= b for a, b in segs)]
    return sorted(edits)

def ld_strings(obj, out, key=None):
    if isinstance(obj, dict):
        for k, v in obj.items(): ld_strings(v, out, k)
    elif isinstance(obj, list):
        for v in obj: ld_strings(v, out, key)
    elif isinstance(obj, str) and key in LD_KEYS and has_words(obj):
        out.append(obj)

def segments_of(path):
    src = open(src_file(path), encoding="utf-8").read()
    segs = []
    for s, e, kind, payload in walk(src):
        if kind == "seg":
            segs.append(to_placeholders(payload)[0])
        elif kind == "attr":
            segs.append(norm(html.unescape(payload)))
        elif kind == "ld":
            body = re.sub(r"^<script[^>]*>|</script>$", "", payload)
            out = []; ld_strings(json.loads(body), out); segs += [norm(x) for x in out]
    return segs

def extract():
    seen, order = {}, []
    for p in PAGES:
        for t in segments_of(p):
            k = sid(t)
            if k not in seen:
                seen[k] = {"en": t, "pages": [p or "/"]}; order.append(k)
            elif (p or "/") not in seen[k]["pages"]:
                seen[k]["pages"].append(p or "/")
    data = {k: seen[k] for k in order}
    json.dump(data, open(os.path.join(HERE, "segments.json"), "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=1)
    chars = sum(len(v["en"]) for v in data.values())
    print("segments:", len(data), "chars:", chars)

def missing(lang):
    segs = json.load(open(os.path.join(HERE, "segments.json"), encoding="utf-8"))
    fn = os.path.join(HERE, lang + ".json")
    tr = json.load(open(fn, encoding="utf-8")) if os.path.exists(fn) else {}
    todo = {k: v["en"] for k, v in segs.items() if k not in tr}
    print(lang, "missing:", len(todo), "of", len(segs))
    return todo

# ---- URL handling
def page_url(lang, p):
    return SITE + "/" + ((lang + "/") if lang != "en" else "") + p

def map_url(u, lang, base_path):
    """Rewrite a URL found in an English page so it works from /<lang>/<base_path>."""
    if not u or u.startswith(("#", "mailto:", "tel:", "javascript:", "data:")):
        return u
    sp = urlsplit(u)
    if sp.scheme and sp.netloc and sp.netloc not in ("marketingkamran.com", "www.marketingkamran.com"):
        return u
    absu = urljoin(SITE + "/" + base_path, u)
    sp = urlsplit(absu)
    path = sp.path.lstrip("/")
    tail = ("?" + sp.query if sp.query else "") + ("#" + sp.fragment if sp.fragment else "")
    key = "" if path in ("", "index.html") else ("blog/" if path in ("blog", "blog/index.html") else path)
    if key in PAGE_SET:
        new = "/" + lang + "/" + key
    else:
        new = "/" + path
    return (SITE + new if u.startswith("http") else new) + tail

def hreflang_block(p):
    lines = ['<link rel="alternate" hreflang="en" href="%s">' % page_url("en", p)]
    for c in LIVE:
        lines.append('<link rel="alternate" hreflang="%s" href="%s">' % (c, page_url(c, p)))
    lines.append('<link rel="alternate" hreflang="x-default" href="%s">' % page_url("en", p))
    return "\n".join(lines)

SWITCH_CSS = ('<style id="lang-sw-css">.lang-sw{position:relative;display:inline-block;font:500 13.5px/1 "Instrument Sans",system-ui,sans-serif;margin-left:14px}'
    '.lang-sw summary{list-style:none;cursor:pointer;padding:8px 10px;border:1px solid rgba(11,33,67,.18);border-radius:8px;color:inherit;white-space:nowrap}'
    '.lang-sw summary::-webkit-details-marker{display:none}.lang-sw summary:after{content:" \\25BE";font-size:11px}'
    '.lang-sw ul{position:absolute;right:0;top:calc(100% + 6px);margin:0;padding:6px;list-style:none;background:#fff;border:1px solid #DDE5F0;border-radius:10px;box-shadow:0 12px 32px -12px rgba(8,26,54,.3);z-index:1000;min-width:140px}'
    '.lang-sw li a{display:block;padding:8px 10px;border-radius:6px;color:#0B2143;text-decoration:none;font-size:14px}'
    '.lang-sw li a:hover,.lang-sw li a[aria-current]{background:#F4F7FB}.nav-links a.nav-item,.topnav a{white-space:nowrap}'
    '@media(max-width:860px){.nav-logo img{min-width:110px}.nav-links{gap:10px}.lang-sw{margin-left:0}.lang-sw summary{padding:7px 8px}}'
    '@media(max-width:400px){.nav-cta{padding:9px 14px;font-size:13px}.topnav .btn{padding:8px 12px;font-size:13px}}.topbar .brand{white-space:nowrap}@media(max-width:620px){.topnav{gap:8px}}@media(max-width:400px){.topbar .brand{font-size:16px}}@media(max-width:480px){.nav-inner>.nav-back{display:none}}@media(max-width:900px){.results-grid{grid-template-columns:repeat(2,minmax(0,1fr))!important}}.result-l,.result-n{overflow-wrap:break-word;hyphens:auto}html:not([lang=en]) :is(h1,h2,h3){overflow-wrap:break-word}@media(max-width:480px){html:not([lang=en]) :is(h1,h2,h3){hyphens:auto}}html:not([lang=en]) .cta .btn{white-space:normal;max-width:100%}</style>')

def switcher(lang, p):
    items = [("en", "English")] + [(c, LANGS[c][0]) for c in LIVE]
    lis = "".join('<li><a href="%s" hreflang="%s" lang="%s"%s>%s</a></li>' % (
        "/" + ("" if c == "en" else c + "/") + p, c, c, ' aria-current="true"' if c == lang else "", n) for c, n in items)
    return '<details class="lang-sw"><summary aria-label="Language">%s</summary><ul>%s</ul></details>' % (lang.upper(), lis)

def insert_switcher(src, lang, p):
    # insertion and removal mirror each other exactly, so rebuilding never drifts
    src = re.sub(r'<details class="lang-sw">.*?</details>', "", src, flags=re.S)
    src = re.sub(r'<style id="lang-sw-css">.*?</style>\n', "", src, flags=re.S)
    if p in NOINDEX:
        return src
    m = re.search(r'<(nav|div)\b[^>]*class="[^"]*\b(topnav|nav-links)\b[^"]*"[^>]*>', src) or \
        re.search(r'<(div)\b[^>]*class="[^"]*\bnav-inner\b[^"]*"[^>]*>', src)
    if not m:
        raise SystemExit("no nav found in " + p)
    tag, depth, i = m.group(1), 0, m.start()
    for t in re.finditer(r"<(/?)%s\b[^>]*>" % tag, src[m.start():]):
        depth += -1 if t.group(1) else 1
        if depth == 0:
            i = m.start() + t.start(); break
    src = src[:i] + switcher(lang, p) + src[i:]
    return src.replace("</head>", SWITCH_CSS + "\n</head>", 1)

def set_head(src, lang, p):
    src = re.sub(r'\n?<link rel="alternate" hreflang="[^"]+" href="[^"]+">', "", src)
    if p not in NOINDEX:
        if '<link rel="canonical"' not in src:
            raise SystemExit("no canonical in " + p)
        src = re.sub(r'(<link rel="canonical" href=")[^"]*(">)', lambda m: m.group(1) + page_url(lang, p) + m.group(2), src, count=1)
        src = re.sub(r'(<link rel="canonical" href="[^"]*">)', lambda m: m.group(1) + "\n" + hreflang_block(p), src, count=1)
    return src

def build_english():
    for p in PAGES:
        fn = src_file(p)
        src = open(fn, encoding="utf-8").read()
        new = insert_switcher(set_head(src, "en", p), "en", p)
        if new != src:
            open(fn, "w", encoding="utf-8", newline="\n").write(new)

def translate_ld(obj, tr, lang, p, key=None):
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            if k == "areaServed" and isinstance(v, list) and all(isinstance(x, dict) and x.get("@type") == "Country" for x in v):
                out[k] = [{"@type": "Country", "name": n} for n in LANGS[lang][2]]
            else:
                out[k] = translate_ld(v, tr, lang, p, k)
        if "@type" in out and out.get("@type") in ("WebPage", "Article", "BlogPosting", "CollectionPage", "Blog"):
            out.setdefault("inLanguage", lang)
            if out.get("inLanguage") == "en": out["inLanguage"] = lang
        return out
    if isinstance(obj, list):
        return [translate_ld(v, tr, lang, p, key) for v in obj]
    if isinstance(obj, str):
        if key in LD_KEYS and has_words(obj):
            return html.unescape(tr[sid(norm(obj))])
        if key in ("inLanguage",):
            return lang
        if key in ("url", "item", "mainEntityOfPage", "contentUrl", "embedUrl", "thumbnailUrl", "image", "logo") \
                and obj.startswith(SITE):
            return map_url(obj, lang, p)
    return obj

JS = json.load(open(os.path.join(HERE, "js.json"), encoding="utf-8"))

def build_consent(lang):
    js = open(os.path.join(ROOT, "consent.js"), encoding="utf-8").read()
    for en_lit, by_lang in JS["consent"].items():
        if en_lit not in js:
            raise SystemExit("consent.js no longer contains: " + en_lit)
        js = js.replace(en_lit, by_lang[lang])
    open(os.path.join(ROOT, "consent-%s.js" % lang), "w", encoding="utf-8", newline="\n").write(js)

def build_lang(lang):
    build_consent(lang)
    tr = json.load(open(os.path.join(HERE, lang + ".json"), encoding="utf-8"))
    missing_ids = []
    for p in PAGES:
        src = open(src_file(p), encoding="utf-8").read()
        src = re.sub(r'<details class="lang-sw">.*?</details>\n?', "", src, flags=re.S)
        out, last = [], 0
        for s, e, kind, payload in walk(src):
            out.append(src[last:s]); last = e
            if kind == "seg":
                ph, tags = to_placeholders(payload)
                t = tr.get(sid(ph))
                if t is None: missing_ids.append(sid(ph)); out.append(payload); continue
                out.append(from_placeholders(t, tags, ph))
            elif kind == "attr":
                t = tr.get(sid(norm(html.unescape(payload))))
                if t is None: missing_ids.append(sid(norm(html.unescape(payload)))); out.append(payload); continue
                out.append(html.escape(html.unescape(t), quote=True))
            elif kind == "ld":
                head = re.match(r"<script[^>]*>", payload).group(0)
                body = payload[len(head):-len("</script>")]
                try:
                    obj = translate_ld(json.loads(body), tr, lang, p)
                except KeyError as ex:
                    missing_ids.append(str(ex)); out.append(payload); continue
                out.append(head + "\n" + json.dumps(obj, ensure_ascii=False, indent=2).replace("</", "<\\/") + "\n</script>")
        out.append(src[last:])
        doc = "".join(out)
        # language attributes
        doc = re.sub(r'<html lang="[^"]*"', '<html lang="%s"' % lang, doc, count=1)
        doc = re.sub(r'(<meta property="og:locale" content=")[^"]*', lambda m: m.group(1) + LANGS[lang][1], doc)
        # URLs in href/src/action/content/value/poster/data-* attributes
        def fix_attr(m):
            name, val = m.group(1), m.group(2)
            if name == "content" and not val.startswith(SITE): return m.group(0)
            if name == "value" and not val.startswith(SITE): return m.group(0)
            return '%s="%s"' % (name, map_url(val, lang, p))
        doc = re.sub(r'\b(href|src|action|content|value|poster|data-img|data-pdf)="([^"]*)"', fix_attr, doc)
        doc = re.sub(r'\b(srcset|imagesrcset)="([^"]*)"', lambda m: '%s="%s"' % (m.group(1), ", ".join(
            " ".join([map_url(part.split()[0], lang, p)] + part.split()[1:])
            for part in m.group(2).split(",") if part.strip())), doc)
        # strings inside inline scripts, and the per-language cookie banner
        for en_lit, by_lang in JS["page"].items():
            if en_lit in doc: doc = doc.replace(en_lit, by_lang[lang])
        doc = doc.replace('src="/consent.js"', 'src="/consent-%s.js"' % lang)
        doc = set_head(doc, lang, p)
        doc = insert_switcher(doc, lang, p)
        outp = os.path.join(ROOT, lang, (p + "index.html") if p == "" or p.endswith("/") else p)
        os.makedirs(os.path.dirname(outp), exist_ok=True)
        open(outp, "w", encoding="utf-8", newline="\n").write(doc)
    if missing_ids:
        raise SystemExit("%s: %d missing translations, e.g. %s" % (lang, len(missing_ids), missing_ids[:5]))

def build_sitemap():
    old = open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read()
    meta = {}
    for m in re.finditer(r"<url>\s*<loc>([^<]+)</loc>(.*?)</url>", old, re.S):
        meta[m.group(1)] = m.group(2)
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for lang in ["en"] + LIVE:
        for p in PAGES:
            if p in NOINDEX: continue
            en = page_url("en", p)
            rest = meta.get(en, "\n    <changefreq>monthly</changefreq>\n")
            rest = re.sub(r"\s*<xhtml:link[^>]*/>", "", rest).rstrip() + "\n"
            lines.append("  <url>\n    <loc>%s</loc>%s" % (page_url(lang, p), rest.rstrip("\n")))
            for c in ["en"] + LIVE:
                lines.append('    <xhtml:link rel="alternate" hreflang="%s" href="%s"/>' % (c, page_url(c, p)))
            lines.append('    <xhtml:link rel="alternate" hreflang="x-default" href="%s"/>' % en)
            lines.append("  </url>")
    lines.append("</urlset>")
    open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")

def merge(lang):
    """Fold _i18n/chunks/<lang>-NN.tsv (id<TAB>text) into _i18n/<lang>.json."""
    import glob
    segs = json.load(open(os.path.join(HERE, "segments.json"), encoding="utf-8"))
    fn = os.path.join(HERE, lang + ".json")
    tr = json.load(open(fn, encoding="utf-8")) if os.path.exists(fn) else {}
    bad = []
    for f in sorted(glob.glob(os.path.join(HERE, "chunks", lang + "-*.tsv"))):
        for line in open(f, encoding="utf-8"):
            line = line.rstrip("\n")
            if not line.strip(): continue
            k, _, t = line.partition("\t")
            if k not in segs: bad.append((f, k)); continue
            ph = sorted(re.findall(r"</?t\d+/?>", segs[k]["en"]))
            if sorted(re.findall(r"</?t\d+/?>", t)) != ph: bad.append((k, "placeholders")); continue
            tr[k] = t
    json.dump(tr, open(fn, "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=0, sort_keys=True)
    print(lang, "translations:", len(tr), "of", len(segs), "problems:", bad[:20])

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "extract": extract()
    elif cmd == "missing":
        todo = missing(sys.argv[2])
        json.dump(todo, open(os.path.join(HERE, "todo-%s.json" % sys.argv[2]), "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=0)
    elif cmd == "merge": merge(sys.argv[2])
    elif cmd == "build":
        for c in LIVE: build_lang(c)
        build_english(); build_sitemap()
        print("built:", ["en"] + LIVE)
