"""
gestures/static/close_1.py
───────────────────────────
Single-hand ✊  Closed Fist
Action: Pause Audio

Fix: pynput Key.media_play_pause doesn't work on Wayland/Hyprland because
pynput uses XTest under the hood which has no effect outside of XWayland.
Using playerctl instead — it speaks MPRIS directly to media players
(Spotify, Firefox, MPV, etc.) and works natively on Hyprland.
"""
from __future__ import annotations
import subprocess

GESTURE_LABEL = "Closed_Fist"
GESTURE_NAME  = "close_1"


def matches(result) -> bool:
    if not result.gestures:
        return False
    fist_count = sum(
        1 for h in result.gestures
        if h and h[0].category_name == GESTURE_LABEL and h[0].score >= 0.70
    )
    return fist_count == 1


def action() -> None:
    try:
        subprocess.Popen(
            ["playerctl", "pause"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
    except Exception as exc:
        print(f"[{GESTURE_NAME}] {exc}")