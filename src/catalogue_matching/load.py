import csv
from pathlib import Path

from catalogue_matching.models import Recording, Work


def _blank_to_none(value: str) -> str | None:
    value = value.strip()
    return value or None


def load_recordings(path: Path) -> list[Recording]:
    with path.open(newline="", encoding="utf-8") as f:
        return [
            Recording(
                recording_id=row["recording_id"],
                title=row["title"],
                artist=row["artist"],
                isrc=_blank_to_none(row["isrc"]),
                streams=int(row["streams"]),
            )
            for row in csv.DictReader(f)
        ]


def load_works(path: Path) -> list[Work]:
    with path.open(newline="", encoding="utf-8") as f:
        return [
            Work(
                work_id=row["work_id"],
                title=row["title"],
                writers=row["writers"],
                iswc=_blank_to_none(row["iswc"]),
            )
            for row in csv.DictReader(f)
        ]


def load_links(path: Path) -> dict[str, str]:
    """Known recording -> work links, like MusicBrainz 'performance' relationships."""
    with path.open(newline="", encoding="utf-8") as f:
        return {row["recording_id"]: row["work_id"] for row in csv.DictReader(f)}
