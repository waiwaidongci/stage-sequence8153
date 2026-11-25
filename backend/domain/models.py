from enum import StrEnum
from typing import Annotated, Literal, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class EventType(StrEnum):
    monitor_dropout = "monitor_dropout"
    cue_restart = "cue_restart"
    prop_hold = "prop_hold"
    lighting_reset = "lighting_reset"
    clean_check = "clean_check"


FaultEvent = Literal[
    EventType.monitor_dropout,
    EventType.cue_restart,
    EventType.prop_hold,
    EventType.lighting_reset,
]
Second = Annotated[int, Field(ge=0, le=86400)]


class Observation(BaseModel):
    model_config = ConfigDict(extra="forbid", allow_inf_nan=False, str_strip_whitespace=True, frozen=True)

    session_id: str = Field(pattern=r"^[A-Za-z0-9][A-Za-z0-9_.-]*$", max_length=64)
    production: str = Field(min_length=1, max_length=80)
    observed_from_s: Second
    observed_through_s: Second
    event_no: int = Field(ge=1, le=1_000_000)
    offset_s: Second
    event_type: EventType
    cue_ref: str = Field(min_length=1, max_length=80)

    @model_validator(mode="after")
    def check_observation_bounds(self) -> Self:
        if not self.observed_from_s <= self.offset_s <= self.observed_through_s:
            raise ValueError("offset_s must fall within the session's observed bounds")
        return self


class AnalysisOptions(BaseModel):
    model_config = ConfigDict(extra="forbid", allow_inf_nan=False, frozen=True)

    antecedent_event: FaultEvent = EventType.monitor_dropout
    consequent_event: FaultEvent = EventType.cue_restart
    control_event: FaultEvent = EventType.prop_hold
    window_start_s: Second = 0
    window_end_s: Second = 300
    max_gap_s: int = Field(default=30, ge=1, le=86400)
    min_complete_sessions: int = Field(default=3, ge=1, le=5000)
    examples_per_sequence: int = Field(default=4, ge=1, le=20)

    @model_validator(mode="after")
    def check_comparison(self) -> Self:
        if len({self.antecedent_event, self.consequent_event, self.control_event}) != 3:
            raise ValueError("antecedent_event, consequent_event and control_event must be distinct")
        if self.window_end_s - self.window_start_s < self.max_gap_s:
            raise ValueError("the observation window must be at least as long as max_gap_s")
        return self
