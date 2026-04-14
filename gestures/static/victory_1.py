"""
gestures/static/point_down_1.py
────────────────────────────────
Single-hand ✌️  Victory
Action: Brightness Down

Note: MediaPipe GestureRecognizer has no dedicated "point down" label.
Victory (✌️) is used here as the closest available label and is distinct
enough from all other bindings to avoid accidental triggers.

Windows: uses screen_brightness_control
Linux:   uses brightnessctl
"""
from __future__ import annotations
import sys

GESTURE_LABEL = "Victory"
GESTURE_NAME  = "victory_1"


def matches(result) -> bool:
    if not result.gestures or len(result.gestures) != 1:
        return False
    top = result.gestures[0][0]
    return top.category_name == GESTURE_LABEL and top.score >= 0.70


def action() -> None:
    try:
        if sys.platform == "win32":
            import screen_brightness_control as sbc
            current = sbc.get_brightness(display=0)[0]
            sbc.set_brightness(max(0, current - 5))
        else:
            import subprocess
            subprocess.Popen(
                ["brightnessctl", "set", "5%-"],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            )
    except Exception as exc:
        print(f"[{GESTURE_NAME}] {exc}")