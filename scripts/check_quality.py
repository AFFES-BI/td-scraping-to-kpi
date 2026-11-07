# Stage 3 helper: finds casing duplicates + checks a few raw texts against what the model returned
import csv, json, re, sys
from collections import defaultdict
ex = json.load(open("data/extracted.json", encoding="utf-8"))["postings"]
groups = defaultdict(set)
for p in ex:
    for s in p["required_skills"]:
        groups[s.lower()].add(s)
print("== Casing duplicates ==")
for k, v in groups.items():
    if len(v) > 1: print(" ", sorted(v))
rows = [r for r in csv.DictReader(open("data/jobs_sample.csv", encoding="utf-8", newline="")) if r["description"].strip()][:12]
KEYS = ["python","sql","docker","aws","azure","gcp","google cloud","kubernetes","java","c++","pytorch","tensorflow","excel","power bi","tableau","terraform","linux","git","javascript","typescript"]
print("\n== Known tools found by plain text search in the 1500 chars the model saw (vs. extracted) ==")
for i,(r,p) in enumerate(zip(rows,ex),1):
    t = r["description"][:1500].lower()
    found = [k for k in KEYS if re.search(r"(?<![a-z+])"+re.escape(k)+r"(?![a-z])", t)]
    got = [s.lower() for s in p["required_skills"]]
    missed = [k for k in found if not any(k in g for g in got)]
    print(f"{i:2d} {r['title'][:40]!r:44} found_in_text={found} MISSED_by_LLM={missed}")
