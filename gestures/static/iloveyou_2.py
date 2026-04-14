from __future__ import annotations
import shutil
import subprocess

GESTURE_LABEL = "ILoveYou"
GESTURE_NAME  = "iloveyou_2"

def matches(result) -> bool:
    if not result.gestures or len(result.gestures) != 2:
        return False
    return all(h[0].category_name == GESTURE_LABEL and h[0].score >= 0.70
               for h in result.gestures)