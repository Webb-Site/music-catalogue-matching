"""Match recordings to works, keeping every unmatched recording with a reason.

Order of evidence:
1. A known link (strongest).
2. Exactly one work with the same normalised title.
3. Otherwise unmatched, with a reason a person can act on.
"""

from collections import defaultdict

from catalogue_matching.models import MatchResult, Recording, Work


def normalise_title(title: str) -> str:
    return " ".join(title.casefold().split())


def unmatched_reason(recording: Recording, candidates: list[Work]) -> str:
    """Explain why `recording` could not be matched.

    `candidates` are the works whose normalised title equals the recording's
    (zero, or two or more: exactly one would have matched).
    """
    # TODO(human): return a short reason code that tells a rights team what to fix.
    return "no_match"


def match_recordings(
    recordings: list[Recording],
    works: list[Work],
    links: dict[str, str],
) -> list[MatchResult]:
    works_by_title: dict[str, list[Work]] = defaultdict(list)
    for work in works:
        works_by_title[normalise_title(work.title)].append(work)

    results: list[MatchResult] = []
    for rec in recordings:
        if rec.recording_id in links:
            results.append(MatchResult(rec, links[rec.recording_id], "link", None))
            continue

        candidates = works_by_title.get(normalise_title(rec.title), [])
        if len(candidates) == 1:
            results.append(MatchResult(rec, candidates[0].work_id, "title", None))
        else:
            results.append(MatchResult(rec, None, None, unmatched_reason(rec, candidates)))
    return results
