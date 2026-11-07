# TD3 — From job postings to a KPI
Pipeline: `scripts/extract_skills.py` (Ollama/qwen3:8b) → `scripts/compute_kpi.py` → `docs/index.html` (dashboard).
Extras: `scrape_demo.py`, `check_quality.py` (Stage 3), `compute_kpi2.py` (second KPI).
Local only (gitignored): `data/jobs_sample.csv`, `data/extracted.json`. Published: `docs/data/kpi.json` (aggregates only).
Run with Python 3.12 (`requests`, `beautifulsoup4`) and Ollama running.
