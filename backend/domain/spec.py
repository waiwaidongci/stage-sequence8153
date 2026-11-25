from collections.abc import Iterable

from .demo import seed
from .models import AnalysisOptions, Observation
from .report import build_report
from .sessions import group_sessions, record_key, validate_rows
from .windows import prepare_windows


TITLE = "社区剧团合成排练故障序列联查"
METHOD = "会话级有向序列支持率、置信度与提升度"
SEED_NAME = "桥边来信-20261125-技术排练"
ROW_MODEL = Observation
OPTIONS_MODEL = AnalysisOptions

__all__ = [
    "TITLE", "METHOD", "SEED_NAME", "ROW_MODEL", "OPTIONS_MODEL",
    "record_key", "validate_rows", "analyze", "seed",
]


def analyze(
    rows: Iterable[Observation | dict], options: AnalysisOptions | dict | None = None,
) -> dict:
    settings = AnalysisOptions.model_validate({} if options is None else options)
    return build_report(prepare_windows(group_sessions(rows), settings), settings)
