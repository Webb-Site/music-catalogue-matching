"""Run matching over a data folder and write the results to DuckDB.

    uv run python -m catalogue_matching.pipeline data/sample catalogue.duckdb
"""

import sys
from pathlib import Path

import duckdb

from catalogue_matching.load import load_links, load_recordings, load_works
from catalogue_matching.match import match_recordings
from catalogue_matching.models import MatchResult
from catalogue_matching.royalties import match_rate, royalties_at_risk


def run(data_dir: Path) -> list[MatchResult]:
    return match_recordings(
        load_recordings(data_dir / "recordings.csv"),
        load_works(data_dir / "works.csv"),
        load_links(data_dir / "links.csv"),
    )


def write_duckdb(results: list[MatchResult], db_path: Path) -> None:
    with duckdb.connect(str(db_path)) as con:
        con.execute(
            """
            CREATE OR REPLACE TABLE match_results (
                recording_id VARCHAR, title VARCHAR, artist VARCHAR, isrc VARCHAR,
                streams BIGINT, work_id VARCHAR, method VARCHAR, reason VARCHAR
            )
            """
        )
        con.executemany(
            "INSERT INTO match_results VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            [
                (
                    r.recording.recording_id, r.recording.title, r.recording.artist,
                    r.recording.isrc, r.recording.streams, r.work_id, r.method, r.reason,
                )
                for r in results
            ],
        )


def main() -> None:
    data_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("data/sample")
    db_path = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("catalogue.duckdb")
    results = run(data_dir)
    write_duckdb(results, db_path)
    print(f"Matched {match_rate(results):.0%} of {len(results)} recordings")
    print(f"Royalties at risk (illustrative): £{royalties_at_risk(results):,.2f}")
    print(f"Results written to {db_path} (table: match_results)")


if __name__ == "__main__":
    main()
