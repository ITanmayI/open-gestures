from __future__ import annotations
import subprocess

GESTURE_LABEL = "Pointing_Up"
GESTURE_NAME  = "point_up_1"

def matches(result) -> bool:
    if not result.gestures:
        return False
    count = sum(
        1 for h in result.gestures
        if h and h[0].category_name == GESTURE_LABEL and h[0].score >= 0.70
    )
    return count == 1