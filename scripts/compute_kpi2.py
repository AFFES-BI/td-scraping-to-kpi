# Second, genuinely different KPI: share of postings naming a cloud provider (word-boundary match, case-insensitive)
import json, re
CLOUD = [r"\baws\b", r"\bamazon web services\b", r"\bazure\b", r"\bgcp\b", r"\bgoogle cloud\b", r"\bs3\b", r"\bsagemaker\b", r"\bbedrock"]
ex = json.load(open("data/extracted.json", encoding="utf-8"))["postings"]
hits = [p for p in ex if any(re.search(c, s.lower()) for s in p["required_skills"] for c in CLOUD)]
print(f"Postings mentioning a cloud provider: {len(hits)}/{len(ex)} = {len(hits)/len(ex):.1%}")
for p in hits: print("  -", p["title"][:50])
