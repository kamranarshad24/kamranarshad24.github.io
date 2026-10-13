"""Every number in an English segment must survive translation (format-insensitive)."""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
lang = sys.argv[1]
segs = json.load(open(os.path.join(HERE, "segments.json"), encoding="utf-8"))
tr = json.load(open(os.path.join(HERE, lang + ".json"), encoding="utf-8"))
def nums(s):
    s = re.sub(r"<[^>]+>|&#x?[0-9a-fA-F]+;|&[a-z]+;", " ", s)
    s = re.sub(r"(?<=\d)[ .,\u202f\u00a0'](?=\d{3}\b)", "", s)   # thousands separators
    return sorted(re.sub(r"[.,]", ".", n) for n in re.findall(r"\d+(?:[.,]\d+)?", s))
bad = 0
for k, v in segs.items():
    if k in tr and nums(v["en"]) != nums(tr[k]):
        bad += 1; print(k, "\n  EN:", v["en"][:160], "\n  TR:", tr[k][:160], "\n  ", nums(v["en"]), nums(tr[k]))
print(lang, "number mismatches:", bad)
