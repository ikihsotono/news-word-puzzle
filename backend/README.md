# Backend (MVP)

## Overview
- Fetch RSS feeds
- Generate 3–5 cloze puzzles
- Write `data/puzzles.json`
- Intended to run hourly (GitHub Actions cron)
- Only runs if local time in America/Los_Angeles is 07:00–07:20 and not already generated today

## Setup
1. Copy config:
   - `cp backend/config.example.json backend/config.json`
2. Install deps:
   - `python -m venv .venv && . .venv/bin/activate`
   - `pip install -r backend/requirements.txt`

## Run
- `python3 backend/run_daily.py`

## Notes
- LLM-based generation is not yet implemented.
- Replace the placeholder logic in `generate_puzzles()` with real AI generation.
- You can force a run (useful for tests) with `NWP_FORCE=1`.
- A local sample config is available at `backend/config.sample.local.json`.
