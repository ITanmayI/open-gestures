"""
gestures/static/close_2.py
───────────────────────────
Double-hand ✊✊  Closed Fist (both hands)
Action: Close Focused Application

Fix 1: replaced len(result.gestures) != 2 strict check with fist_count == 2
        to handle mediapipe's inconsistent slot counts in LIVE_STREAM mode.
Fix 2: dropped pynput (broken on Wayland/Hyprland) — using hyprctl dispatch
        killactive instead, which is the correct Hyprland-native IPC call.
        No keybind required, works regardless of what window is focused.
"""
from __future__ import annotations
import subprocess

GESTURE_LABEL = "Closed_Fist"
GESTURE_NAME  = "close_2"


def matches(result) -> bool:
    if not result.gestures:
        return False
    fist_count = sum(
        1 for h in result.gestures
        if h and h[0].category_name == GESTURE_LABEL and h[0].score >= 0.70
    )
    return fist_count == 2


def action() -> None:
    try:
        subprocess.Popen(
            ["hyprctl", "dispatch", "killactive"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
    except Exception as exc:
        print(f"[{GESTURE_NAME}] {exc}")