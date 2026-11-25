"""Estimate the publishing royalties that unmatched recordings put at risk.

The rate below is an illustrative assumption for this demo, not a real
industry figure. Real rates vary by service, country and deal.
"""

from catalogue_matching.models import MatchResult

ILLUSTRATIVE_RATE_GBP_PER_STREAM = 0.0005


def royalties_at_risk(
    results: list[MatchResult], rate: float = ILLUSTRATIVE_RATE_GBP_PER_STREAM
) -> float:
    return sum(r.recording.streams for r in results if not r.matched) * rate


def match_rate(results: list[MatchResult]) -> float:
    if not results:
        return 0.0
    return sum(r.matched for r in results) / len(results)
