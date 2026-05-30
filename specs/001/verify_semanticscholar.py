"""Cross-verify citations via the Semantic Scholar Graph API (api.semanticscholar.org).
Second independent source alongside arXiv. Honesty tool: prints the real title, year, venue,
authors, and citation count for each work, so the bibliography is API-grounded, not guessed.
No API key needed for low-volume use; respects rate limits with a delay."""
import json
import time
import urllib.parse
import urllib.request

BASE = "https://api.semanticscholar.org/graph/v1/paper/"
FIELDS = "title,year,venue,authors,citationCount,externalIds"

# (label, lookup) - lookup is "arXiv:ID" or "search:query"
WORKS = [
    ("SecureDNA screening", "arXiv:2403.14023"),
    ("Know Your Scientist", "arXiv:2602.06172"),
    ("KYChain (KYC prior art)", "arXiv:2001.01659"),
    ("SSI KYC framework (prior art)", "arXiv:2112.01237"),
    ("Microsoft Paraphrase Project", "search:AI protein design evade DNA synthesis screening biosecurity"),
    ("W3C Verifiable Credentials", "search:Verifiable Credentials Data Model W3C"),
]


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "synth-attest-citecheck/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8", "replace"))


def show(p, indent="  "):
    auth = ", ".join(a.get("name", "?") for a in (p.get("authors") or [])[:6])
    extra = "" if len(p.get("authors") or []) <= 6 else " (+ more)"
    ext = p.get("externalIds") or {}
    print(f"{indent}TITLE : {p.get('title')}")
    print(f"{indent}YEAR  : {p.get('year')}   VENUE: {p.get('venue')}   CITES: {p.get('citationCount')}")
    print(f"{indent}AUTHRS: {auth}{extra}")
    print(f"{indent}IDS   : " + ", ".join(f"{k}={v}" for k, v in ext.items()))


print("=== Semantic Scholar cross-verification ===\n")
for label, lookup in WORKS:
    print("WORK:", label)
    try:
        if lookup.startswith("arXiv:"):
            p = get(BASE + "arXiv:" + lookup.split(":", 1)[1] + "?fields=" + FIELDS)
            show(p)
        else:
            q = lookup.split(":", 1)[1]
            url = "https://api.semanticscholar.org/graph/v1/paper/search?" + urllib.parse.urlencode(
                {"query": q, "limit": 3, "fields": FIELDS})
            res = get(url)
            data = res.get("data") or []
            if not data:
                print("  no match")
            for p in data[:3]:
                show(p, indent="    - ")
                print()
    except urllib.error.HTTPError as e:
        print("  HTTP", e.code, "(rate limit or not indexed)")
    except Exception as e:
        print("  error:", e)
    print()
    time.sleep(3.5)  # Semantic Scholar courtesy delay (unauthenticated)
