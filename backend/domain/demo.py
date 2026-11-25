from .models import EventType


PRODUCTION = "《桥边来信》"
CHECK = EventType.clean_check.value
DROPOUT = EventType.monitor_dropout.value
RESTART = EventType.cue_restart.value
PROP = EventType.prop_hold.value
LIGHT = EventType.lighting_reset.value

# Bounds and cue-log lines for each synthetic run, in stage manager order.
RUNS = (
    (0, 300, ((0, CHECK, "STG-00"), (40, DROPOUT, "SND-07"), (45, LIGHT, "LX-07"),
              (70, RESTART, "GO-08"), (100, DROPOUT, "SND-09"), (105, RESTART, "GO-09"))),
    (0, 340, ((12, PROP, "PROP-02"), (25, DROPOUT, "SND-03"), (25, RESTART, "GO-03"),
              (330, LIGHT, "LX-18"))),
    (0, 300, ((0, CHECK, "STG-00"), (70, RESTART, "GO-08"), (82, DROPOUT, "SND-10"),
              (125, RESTART, "GO-11"))),
    (0, 300, ((75, DROPOUT, "SND-08"), (106, RESTART, "GO-09"), (109, PROP, "PROP-10"))),
    (0, 300, ((265, PROP, "PROP-16"), (270, DROPOUT, "SND-17"), (300, RESTART, "GO-18"))),
    (0, 300, ((271, DROPOUT, "SND-17"), (290, RESTART, "GO-18"))),
    (0, 300, ((22, PROP, "PROP-02"), (40, RESTART, "GO-03"), (70, LIGHT, "LX-08"))),
    (0, 300, ((20, DROPOUT, "SND-03"), (25, RESTART, "GO-03"), (290, PROP, "PROP-18"))),
    (0, 300, ((15, PROP, "PROP-02"), (45, LIGHT, "LX-07"))),
    (0, 300, ((0, CHECK, "STG-00"), (300, CHECK, "STG-18"))),
    (0, 300, ((101, PROP, "PROP-09"),)),
    (0, 300, ((211, LIGHT, "LX-14"),)),
    (0, 300, ((0, CHECK, "STG-00"),)),
    (0, 300, ((300, CHECK, "STG-18"),)),
    (12, 340, ((40, DROPOUT, "SND-07"), (45, RESTART, "GO-07"))),
    (0, 280, ((70, DROPOUT, "SND-08"), (80, RESTART, "GO-08"))),
    (15, 275, ((78, DROPOUT, "SND-08"), (85, RESTART, "GO-09"))),
)


def seed() -> list[dict]:
    return [
        {
            "session_id": f"BRIDGE-{session_number:03d}",
            "production": PRODUCTION,
            "observed_from_s": start,
            "observed_through_s": end,
            "event_no": event_no,
            "offset_s": offset,
            "event_type": kind,
            "cue_ref": cue,
        }
        for session_number, (start, end, events) in enumerate(RUNS, 1)
        for event_no, (offset, kind, cue) in enumerate(events, 1)
    ]
