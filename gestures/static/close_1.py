from __future__ import annotations
import subprocess

GESTURE_LABEL = "Closed_Fist"
GESTURE_NAME  = "close_1"


def matches(result) -> bool:
    if not result.gestures:
        return False
    fist_count = sum(
        1 for h in result.gestures
        if h and h[0].category_name == GESTURE_LABEL and h[0].score >= 0.70
    )
    return fist_count == 1