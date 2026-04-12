"""
gestures/static/open_1.py
──────────────────────────
Single-hand 👋  Open Palm
Action: Play Audio

Fix: same Wayland/pynput issue as close_1 — using playerctl play instead
of Key.media_play_pause. playerctl talks MPRIS directly so it works on
Hyprland without needing XTest or any X11 compatibility layer.
"""
from __future__ import annotations
import subprocess

GESTURE_LABEL = "Open_Palm"
GESTURE_NAME  = "open_1"


def matches(result) -> bool:
    if not result.gestures:
        return False
    open_count = sum(
        1 for h in result.gestures
        if h and h[0].category_name == GESTURE_LABEL and h[0].score >= 0.60
    )
    return open_count == 1


def action() -> None:
    try:
        subprocess.Popen(
            ["playerctl", "play"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
    except Exception as exc:
        print(f"[{GESTURE_NAME}] {exc}")