from __future__ import annotations
import subprocess

GESTURE_LABEL = "Open_Palm"
GESTURE_NAME  = "open_1"


def matches(result) -> bool:
    if not result.gestures:
        return False
    open_count = sum(
        1 for h in result.gestures
        if h and h[0].category_name == GESTURE_LABEL and h[0].score >= 0.60
    )
    return open_count == 1