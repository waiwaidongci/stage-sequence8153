from .sequences import SequenceScan
from .sessions import record_key
from .windows import SessionWindow


def coverage_evidence(windows: list[SessionWindow]) -> list[dict]:
    return [
        {
            "session_id": window.session.session_id,
            "production": window.session.production,
            "observed_from_s": window.session.observed_from_s,
            "observed_through_s": window.session.observed_through_s,
            "status": window.status,
            "observations_in_window": sum(map(len, window.events_by_type.values())),
        }
        for window in windows
    ]


def sequence_evidence(scans: list[SequenceScan], examples_per_sequence: int) -> list[dict]:
    examples = []
    for scan in scans:
        for match in scan.matches[:examples_per_sequence]:
            anchor, target = match.anchor, match.target
            examples.append({
                "sequence": scan.rule.name,
                "session_id": anchor.session_id,
                "production": anchor.production,
                "antecedent_key": record_key(anchor),
                "antecedent_event_no": anchor.event_no,
                "antecedent_event": anchor.event_type.value,
                "antecedent_offset_s": anchor.offset_s,
                "antecedent_cue_ref": anchor.cue_ref,
                "consequent_key": record_key(target),
                "consequent_event_no": target.event_no,
                "consequent_event": target.event_type.value,
                "consequent_offset_s": target.offset_s,
                "consequent_cue_ref": target.cue_ref,
                "gap_s": match.gap_s,
            })
    return examples
