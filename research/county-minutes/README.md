# Bear Lake County Planning Precedents Database

Source: [Bear Lake County Planning & Zoning](https://www.bearlakecounty.info/planning-and-zoning.html) and [Commissioners minutes](https://www.bearlakecounty.info/meetings.html). The county notes posted minutes are convenience copies; official signed minutes are at county offices.

## Purpose
Build a durable, searchable, page-referenced archive for Lanark land-use research, especially Agricultural zoning, hunting lodge/rental cabins, dude ranches, CUPs, recreational lodging, subdivisions, multiple structures and access.

## Status
The collector and index schema are committed. **Do not assume the archive is populated until a successful workflow has produced the manifest and SQLite file.** The initial scope is Planning & Zoning 2024–2026. County Commissioners and older minutes are subsequent phases.

## Storage
- `data/manifest.json`: exact county PDF URLs, retrieval status, hashes and page counts.
- `data/minutes.sqlite`: document metadata, extracted page text and SQLite FTS5 full-text index.
- Each indexed hit retains document ID, source URL and PDF page number.
- Missing PDFs, unreadable scans and failures remain explicitly flagged.
- A later structured decisions table should separately distinguish applicant proposal, P&Z recommendation, commissioners' final decision, conditions and source page.

## Local usage
```bash
pip install requests beautifulsoup4 pypdf
python research/county-minutes/collect.py --groups planning --years 2024 2025 2026
python research/county-minutes/search.py "conditional use"
```

This index is a research aid, not an authoritative legal opinion. Avoid treating proposed uses or discussion as approved precedent.
