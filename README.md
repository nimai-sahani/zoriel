# Zoriel Consumer — v0.3.0

Zoriel's existing v0.2.1 consumer pilot, incrementally migrated into a maintainable service/package structure.

## v0.3.0
- Structured `ZorielIntent` contract
- Dedicated intent parser
- Dedicated catalogue/search service
- Provider-agnostic commerce boundary
- Existing consumer UI and discovery data preserved
- Tests for Hinglish requests, budgets, time extraction and ambiguity

## What is NOT live
- Direct ONDC transaction APIs / production Buyer NP credentials
- In-app payment
- Guaranteed live stock/price/ETA verification
- Production LLM agent orchestration

## Run

```bash
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app:app --reload
```

Open http://127.0.0.1:8000

## Test

```bash
python -m pytest -q
```
