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
Fix 3: replaced hardcoded hyprctl call with cross-platform CloseWindow action
        so the gesture works on both Linux (Hyprland) and Windows.
"""
from __future__ import annotations
from actions.close_window import CloseWindow

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
    CloseWindow().execute()