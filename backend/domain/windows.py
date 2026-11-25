from collections import defaultdict
from dataclasses import dataclass

from .models import AnalysisOptions, EventType, Observation
from .sessions import Session


@dataclass(frozen=True)
class SessionWindow:
    session: Session
    status: str
    events_by_type: dict[EventType, list[Observation]]
    last_eligible_anchor_s: int

    @property
    def complete(self) -> bool:
        return self.status == "complete"


def coverage_status(session: Session, start: int, end: int) -> str:
    left_truncated = session.observed_from_s > start
    right_truncated = session.observed_through_s < end
    if left_truncated and right_truncated:
        return "both_truncated"
    if left_truncated:
        return "left_truncated"
    if right_truncated:
        return "right_truncated"
    return "complete"


def prepare_windows(sessions: list[Session], options: AnalysisOptions) -> list[SessionWindow]:
    result = []
    for session in sessions:
        by_type: dict[EventType, list[Observation]] = defaultdict(list)
        for event in session.events:
            if options.window_start_s <= event.offset_s <= options.window_end_s:
                by_type[event.event_type].append(event)
        result.append(SessionWindow(
            session=session,
            status=coverage_status(session, options.window_start_s, options.window_end_s),
            events_by_type=dict(by_type),
            last_eligible_anchor_s=options.window_end_s - options.max_gap_s,
        ))
    return result
