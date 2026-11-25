# Music Catalogue Matching

[![CI](https://github.com/Webb-Site/music-catalogue-matching/actions/workflows/ci.yml/badge.svg)](https://github.com/Webb-Site/music-catalogue-matching/actions/workflows/ci.yml)

**Status: in progress.** Working on synthetic sample data; MusicBrainz ingestion is next.

Matches music **recordings** (ISRC) to the songwriters' **works** (ISWC) they use, keeps every unmatched recording with a reason a rights team can act on, and estimates the publishing royalties those gaps put at risk.

## Why

When a recording can't be matched to its composition, the songwriter's share of the royalties often goes unpaid. Most pipelines drop or hide those rows. This one keeps them, explains them, and puts a number on them.

## How it works

1. **Known links first.** A recording with an explicit recording-to-work link (like a MusicBrainz "performance" relationship) is matched.
2. **Then unique titles.** If exactly one work has the same normalised title, it's matched.
3. **Otherwise unmatched, with a reason.** No recording is dropped.
4. **Royalties at risk.** Unmatched streams × an illustrative per-stream rate.

## Run it

```bash
uv sync
uv run pytest
uv run python -m catalogue_matching.pipeline data/sample catalogue.duckdb
uv run streamlit run app.py
```

## Roadmap

- [x] Matching core, reasons for unmatched recordings, royalties estimate
- [x] DuckDB output, Streamlit view, tests and CI
- [ ] Richer unmatched reasons (ambiguous titles, versions such as "Live", missing ISRCs)
- [ ] Ingest real recordings and works from the MusicBrainz API or data dumps
- [ ] Fuzzy title matching with a confidence score

## Notes

The sample data is synthetic: artists, titles and codes are made up. The royalty rate is an illustrative assumption, not a real industry figure.
