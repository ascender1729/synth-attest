"""Verify cited works against the live arXiv API (export.arxiv.org/api/query).
Honesty tool: prints CONFIRMED/NOT-FOUND + the real title for each arXiv claim, and flags
non-arXiv works (Science, W3C, bills, gov guidance) as 'verify elsewhere'. No agent guessing."""
import json
import time
import urllib.parse
import urllib.request

API = "http://export.arxiv.org/api/query?"

# (label, arxiv_id_or_None, search_title)
CITES = [
    ("Know Your Scientist (Feldman et al.)", "2602.06172", "Know Your Scientist KYC biosecurity"),
    ("SecureDNA screening", "2403.14023", "SecureDNA verifiably privately screening DNA synthesis"),
    ("Microsoft Paraphrase Project", None, "AI protein design evade nucleic acid synthesis screening"),
    ("Model organisms for emergent misalignment (Turner)", "2506.11613", "model organisms emergent misalignment"),
]


def q(params):
    url = API + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "synth-attest-citecheck/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def titles(xml):
    # crude entry-title extraction (avoid the feed <title> at index 0)
    out = []
    for chunk in xml.split("<entry>")[1:]:
        a = chunk.find("<title>")
        b = chunk.find("</title>")
        if a != -1 and b != -1:
            out.append(" ".join(chunk[a + 7:b].split()))
        a2 = chunk.find("<id>")
        b2 = chunk.find("</id>")
        if a2 != -1 and b2 != -1:
            out[-1] = out[-1] + "  [" + chunk[a2 + 4:b2].strip() + "]"
    return out


print("=== arXiv citation verification ===\n")
for label, aid, title in CITES:
    print("CITE:", label)
    if aid:
        try:
            xml = q({"id_list": aid})
            t = titles(xml)
            if t and "Error" not in t[0]:
                print("  id", aid, "-> FOUND:", t[0])
            else:
                print("  id", aid, "-> NOT FOUND by id; trying title search")
                xml2 = q({"search_query": "all:" + title, "max_results": 3})
                for x in titles(xml2)[:3]:
                    print("     candidate:", x)
        except Exception as e:
            print("  id", aid, "-> API error:", e)
    else:
        print("  (non-arXiv claim; title-search arXiv for any preprint)")
        try:
            xml2 = q({"search_query": "all:" + title, "max_results": 3})
            cands = titles(xml2)[:3]
            if cands:
                for x in cands:
                    print("     arXiv candidate:", x)
            else:
                print("     no arXiv match (expected if it is a Science/journal-only paper)")
        except Exception as e:
            print("  title search error:", e)
    print()
    time.sleep(3)  # arXiv API courtesy delay
print("Non-arXiv works to verify by other means: Microsoft Paraphrase (Science 2025),")
print("W3C VC/DID (w3.org Recommendations), US S.3741 (congress.gov), UK DSIT (gov.uk), ISO 20688-2 (iso.org).")
