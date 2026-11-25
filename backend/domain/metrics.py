from .sequences import SequenceScan


def ratio(numerator: int, denominator: int) -> float | None:
    return numerator / denominator if denominator else None


def sequence_metrics(scan: SequenceScan, complete_sessions: int) -> dict:
    matched = len(scan.matches)
    confidence = ratio(matched, scan.eligible_anchor_sessions)
    baseline = ratio(scan.baseline_sessions, complete_sessions)
    lift = confidence / baseline if confidence is not None and baseline else None
    return {
        "sequence": scan.rule.name,
        "antecedent_event": scan.rule.antecedent.value,
        "consequent_event": scan.rule.consequent.value,
        "complete_sessions": complete_sessions,
        "matched_sessions": matched,
        "eligible_anchor_sessions": scan.eligible_anchor_sessions,
        "baseline_sessions": scan.baseline_sessions,
        "support": ratio(matched, complete_sessions),
        "confidence": confidence,
        "baseline_rate": baseline,
        "lift": lift,
    }
