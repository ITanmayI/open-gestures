"""
gestures/static/point_up_2.py
──────────────────────────────
Double-hand ☝️☝️  Pointing Up (both hands)
Action: Zoom In (Ctrl++)

Fix: using ydotool with raw keycodes — the only reliable method on
Hyprland/Wayland. Daemon (ydotoold) must be running.
Start it with: sudo ydotoold &
Or add it to your Hyprland config: exec-once = ydotoold

Keycodes: 29 = Left Ctrl, 13 = Equal/Plus key
Format: <keycode>:1 = press, <keycode>:0 = release
"""
from __future__ import annotations
import subprocess

GESTURE_LABEL = "Pointing_Up"
GESTURE_NAME  = "point_up_2"


def matches(result) -> bool:
    if not result.gestures:
        return False
    count = sum(
        1 for h in result.gestures
        if h and h[0].category_name == GESTURE_LABEL and h[0].score >= 0.70
    )
    return count == 2


def action() -> None:
    try:
        # Ctrl+= (zoom in): press ctrl, press equal, release equal, release ctrl
        subprocess.Popen(
            ["ydotool", "key", "29:1", "13:1", "13:0", "29:0"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
    except Exception as exc:
        print(f"[{GESTURE_NAME}] {exc}")