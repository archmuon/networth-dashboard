# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Privacy & Network Policy

Read `GLOBAL_PREFERENCES.md` and `REQUIREMENTS.md` before making any changes. Key rules:
- **Zero network requests at runtime** — no CDN, no external fonts, no APIs
- Financial data (`data/networth.json`) must never be committed to the repo
- The spreadsheet files (`*.numbers`, `*.xlsx`) must never be uploaded anywhere

## Running the Dashboard

```bash
pip install -r requirements.txt   # one-time
python server.py                   # starts at http://127.0.0.1:5000
```

## File Structure

```
server.py                  ← Flask backend (routes, data read/write)
index.html                 ← Dashboard frontend (no financial data)
static/
  chart.umd.min.js         ← Chart.js 4.4.3, served locally (no CDN)
data/
  networth.json            ← Financial data — gitignored, never commit
REQUIREMENTS.md            ← Binding project requirements
GLOBAL_PREFERENCES.md      ← Binding global preferences
Networth_Monthly.numbers   ← Source spreadsheet (read-only reference)
Networth_Monthly.xslx.xlsx ← Exported XLSX (read-only reference)
```

## Architecture

`server.py` is the only backend — it serves `index.html` and static assets, and exposes a minimal localhost API:

| Route | Method | Purpose |
|---|---|---|
| `/` | GET | Serve index.html |
| `/api/data` | GET | Read data/networth.json |
| `/api/data` | POST | Write full state to data/networth.json |
| `/api/export` | GET | Download data/networth.json as a file |
| `/static/<file>` | GET | Serve bundled assets (Chart.js) |

All `fetch()` calls in `index.html` target `localhost` only. No data leaves the machine.

## Compliance Check

Run before any commit:
```bash
grep -rn "googleapis\|gstatic\|cdnjs\|jsdelivr\|unpkg\|cloudflare" \
  --include="*.html" --include="*.py" .
# Must return zero results
```

## Versioning

Semantic versioning (`MAJOR.MINOR.PATCH`). Update `VERSION` in `server.py` with every release.

## Working with the Spreadsheet

`Networth_Monthly.numbers` is a binary Apple Numbers format. To read it programmatically, export to XLSX from Numbers first. The equivalent `Networth_Monthly.xslx.xlsx` is already provided. Use `openpyxl` to parse — but do not commit any extracted data to the repo.
