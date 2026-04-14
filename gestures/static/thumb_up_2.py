from __future__ import annotations

GESTURE_LABEL = "Thumb_Up"
GESTURE_NAME  = "thumb_up_2"

def matches(result) -> bool:
    if not result.gestures or len(result.gestures) != 2:
        return False
    return all(h[0].category_name == GESTURE_LABEL and h[0].score >= 0.70
               for h in result.gestures)