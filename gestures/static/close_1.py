from __future__ import annotations
 
GESTURE_LABEL = "Closed_Fist"
GESTURE_NAME  = "closed_1"
 
def matches(result) -> bool:
    if not result.gestures:
        return False
    closed_count = sum(
        1 for h in result.gestures
        if h and h[0].category_name == GESTURE_LABEL and h[0].score >= 0.60
    )
    return closed_count == 1