from .evidence import coverage_evidence, sequence_evidence
from .metrics import sequence_metrics
from .models import AnalysisOptions
from .sequences import comparison_rules, scan_sequence
from .windows import SessionWindow


def build_report(windows: list[SessionWindow], options: AnalysisOptions) -> dict:
    complete = [window for window in windows if window.complete]
    incomplete_count = len(windows) - len(complete)
    scans = [scan_sequence(rule, complete, options.max_gap_s) for rule in comparison_rules(options)]
    sequences = [sequence_metrics(scan, len(complete)) for scan in scans]

    warnings = []
    if incomplete_count:
        warnings.append(f"{incomplete_count} 个观察窗口不完整的场次已排除，详见 session_windows。")
    if len(complete) < options.min_complete_sessions:
        warnings.append(f"完整场次 {len(complete)} 个，低于发布门槛 {options.min_complete_sessions} 个。")
    for sequence in sequences:
        if sequence["lift"] is None:
            warnings.append(f"{sequence['sequence']} 缺少完整场次、合格前项或非零后项基准，提升度无定义。")

    forward = sequences[0]
    return {
        "summary": {
            "session_count": len(windows),
            "complete_sessions": len(complete),
            "excluded_sessions": incomplete_count,
            "observation_count": sum(len(window.session.events) for window in windows),
            "window_start_s": options.window_start_s,
            "window_end_s": options.window_end_s,
            "max_gap_s": options.max_gap_s,
            "min_complete_sessions": options.min_complete_sessions,
            "examples_per_sequence": options.examples_per_sequence,
            "last_eligible_anchor_s": options.window_end_s - options.max_gap_s,
            "forward_matched_sessions": forward["matched_sessions"],
            "forward_lift": forward["lift"],
        },
        "tables": {
            "sequences": sequences,
            "session_windows": coverage_evidence(windows),
            "sequence_examples": sequence_evidence(scans, options.examples_per_sequence),
        },
        "warnings": warnings,
        "publishable": len(complete) >= options.min_complete_sessions and forward["lift"] is not None,
    }
