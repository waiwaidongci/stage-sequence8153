from dataclasses import dataclass

from .models import AnalysisOptions, EventType, Observation
from .windows import SessionWindow


@dataclass(frozen=True)
class SequenceRule:
    name: str
    antecedent: EventType
    consequent: EventType


@dataclass(frozen=True)
class SequenceMatch:
    anchor: Observation
    target: Observation

    @property
    def gap_s(self) -> int:
        return self.target.offset_s - self.anchor.offset_s


@dataclass(frozen=True)
class SequenceScan:
    rule: SequenceRule
    eligible_anchor_sessions: int
    baseline_sessions: int
    matches: list[SequenceMatch]


def comparison_rules(options: AnalysisOptions) -> tuple[SequenceRule, ...]:
    return (
        SequenceRule("forward", options.antecedent_event, options.consequent_event),
        SequenceRule("reverse", options.consequent_event, options.antecedent_event),
        SequenceRule("control", options.control_event, options.consequent_event),
    )


def first_match(
    anchors: list[Observation],
    targets: list[Observation],
    last_anchor_s: int,
    max_gap_s: int,
) -> SequenceMatch | None:
    target_index = 0
    for anchor in anchors:
        if anchor.offset_s > last_anchor_s:
            break
        while target_index < len(targets) and targets[target_index].event_no <= anchor.event_no:
            target_index += 1
        if target_index == len(targets):
            break
        target = targets[target_index]
        if target.offset_s - anchor.offset_s <= max_gap_s:
            return SequenceMatch(anchor, target)
    return None


def scan_sequence(
    rule: SequenceRule,
    complete_windows: list[SessionWindow],
    max_gap_s: int,
) -> SequenceScan:
    eligible_anchor_sessions = baseline_sessions = 0
    matches = []
    for window in complete_windows:
        anchors = window.events_by_type.get(rule.antecedent, [])
        targets = window.events_by_type.get(rule.consequent, [])
        baseline_sessions += bool(targets)
        if not anchors or anchors[0].offset_s > window.last_eligible_anchor_s:
            continue
        eligible_anchor_sessions += 1
        match = first_match(anchors, targets, window.last_eligible_anchor_s, max_gap_s)
        if match is not None:
            matches.append(match)
    return SequenceScan(rule, eligible_anchor_sessions, baseline_sessions, matches)
