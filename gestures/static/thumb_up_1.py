from __future__ import annotations

GESTURE_LABEL = "Thumb_Up"
GESTURE_NAME  = "thumb_up_1"

def matches(result) -> bool:
    if not result.gestures or len(result.gestures) != 1:
        return False
    top = result.gestures[0][0]
    return top.category_name == GESTURE_LABEL and top.score >= 0.70