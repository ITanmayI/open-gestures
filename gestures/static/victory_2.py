

"""
gestures/static/point_down_2.py
────────────────────────────────
Double-hand ✌️✌️  Victory (both hands)
Action: Zoom Out (Ctrl+-)

Fix: using ydotool with raw keycodes — the only reliable method on
Hyprland/Wayland. Daemon (ydotoold) must be running.
Start it with: sudo ydotoold &
Or add it to your Hyprland config: exec-once = ydotoold

Keycodes: 29 = Left Ctrl, 12 = Minus key
Format: <keycode>:1 = press, <keycode>:0 = release
"""
from __future__ import annotations
import subprocess

GESTURE_LABEL = "Victory"
GESTURE_NAME  = "victory_2"


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
            ["ydotool", "key", "29:1", "12:1", "12:0", "29:0"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
    except Exception as exc:
        print(f"[{GESTURE_NAME}] {exc}")