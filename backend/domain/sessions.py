from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass

from .models import Observation


@dataclass(frozen=True)
class Session:
    session_id: str
    production: str
    observed_from_s: int
    observed_through_s: int
    events: tuple[Observation, ...]


def record_key(row: Observation | dict) -> str:
    observation = Observation.model_validate(row)
    return f"{observation.session_id}:{observation.event_no}"


def group_sessions(rows: Iterable[Observation | dict]) -> list[Session]:
    by_session: dict[str, list[Observation]] = defaultdict(list)
    for row in rows:
        event = Observation.model_validate(row)
        by_session[event.session_id].append(event)
    if not by_session:
        raise ValueError("provide at least one rehearsal observation")

    sessions = []
    for session_id, events in sorted(by_session.items()):
        events.sort(key=lambda event: event.event_no)
        first = events[0]
        metadata = (first.production, first.observed_from_s, first.observed_through_s)
        for event in events[1:]:
            if (event.production, event.observed_from_s, event.observed_through_s) != metadata:
                raise ValueError(f"session {session_id}: production and observed bounds must agree")
        for previous, event in zip(events, events[1:]):
            if event.event_no == previous.event_no:
                raise ValueError(f"duplicate observation {record_key(event)}")
            if event.offset_s < previous.offset_s:
                raise ValueError(f"session {session_id}: offsets decrease at event {event.event_no}")
        sessions.append(Session(session_id, *metadata, tuple(events)))
    return sessions


def validate_rows(rows: Iterable[Observation | dict]) -> None:
    group_sessions(rows)
