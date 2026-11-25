from dataclasses import dataclass


@dataclass(frozen=True)
class Recording:
    """A released recording (identified by ISRC in the real world)."""

    recording_id: str
    title: str
    artist: str
    isrc: str | None
    streams: int


@dataclass(frozen=True)
class Work:
    """A songwriters' composition (identified by ISWC in the real world)."""

    work_id: str
    title: str
    writers: str
    iswc: str | None


@dataclass(frozen=True)
class MatchResult:
    """The outcome for one recording: matched to a work, or unmatched with a reason."""

    recording: Recording
    work_id: str | None
    method: str | None  # "link" or "title" when matched
    reason: str | None  # why it is unmatched; None when matched

    @property
    def matched(self) -> bool:
        return self.work_id is not None
