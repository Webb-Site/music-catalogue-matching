from pathlib import Path

import duckdb
import pytest

from catalogue_matching.match import match_recordings, normalise_title
from catalogue_matching.models import Recording, Work
from catalogue_matching.pipeline import run, write_duckdb
from catalogue_matching.royalties import match_rate, royalties_at_risk

SAMPLE = Path(__file__).parent.parent / "data" / "sample"


def rec(rid: str, title: str, streams: int = 1000, isrc: str | None = "GBXYZ0000001") -> Recording:
    return Recording(rid, title, "Artist", isrc, streams)


def work(wid: str, title: str) -> Work:
    return Work(wid, title, "Writer", None)


def test_normalise_title_ignores_case_and_spacing() -> None:
    assert normalise_title("  Paper   KITES ") == "paper kites"


def test_known_link_wins_over_title() -> None:
    [result] = match_recordings([rec("R1", "Home")], [work("W1", "Home"), work("W2", "Home")], {"R1": "W2"})
    assert (result.work_id, result.method) == ("W2", "link")


def test_single_title_candidate_matches() -> None:
    [result] = match_recordings([rec("R1", "paper kites")], [work("W1", "Paper Kites")], {})
    assert (result.work_id, result.method, result.reason) == ("W1", "title", None)


@pytest.mark.parametrize("works", [[], [work("W1", "Home"), work("W2", "Home")]])
def test_unmatched_recordings_are_kept_with_a_reason(works: list[Work]) -> None:
    [result] = match_recordings([rec("R1", "Home")], works, {})
    assert not result.matched
    assert result.reason  # never silently dropped, never blank


def test_royalties_at_risk_counts_only_unmatched() -> None:
    results = match_recordings(
        [rec("R1", "Matched", streams=1000), rec("R2", "Orphan", streams=2000)],
        [work("W1", "Matched")],
        {},
    )
    assert royalties_at_risk(results, rate=0.01) == pytest.approx(20.0)
    assert match_rate(results) == 0.5


def test_sample_pipeline_keeps_every_recording(tmp_path: Path) -> None:
    results = run(SAMPLE)
    assert len(results) == 10
    write_duckdb(results, tmp_path / "out.duckdb")
    with duckdb.connect(str(tmp_path / "out.duckdb")) as con:
        row = con.execute("SELECT count(*), count(*) FILTER (WHERE work_id IS NULL AND reason IS NULL) FROM match_results").fetchone()
    assert row == (10, 0)
