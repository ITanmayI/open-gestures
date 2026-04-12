"""
gestures/static/open_2.py
──────────────────────────
Double-hand 👋👋  Open Palm (both hands)
Action: Open Default Web Browser

Fix: replaced len(result.gestures) != 2 strict check with a counted match,
same pattern as close_1/open_1 — avoids false negatives from mediapipe
returning inconsistent slot counts in LIVE_STREAM mode.
"""
from __future__ import annotations

GESTURE_LABEL = "Open_Palm"
GESTURE_NAME  = "open_2"


def matches(result) -> bool:
    if not result.gestures:
        return False
    open_count = sum(
        1 for h in result.gestures
        if h and h[0].category_name == GESTURE_LABEL and h[0].score >= 0.60
    )
    return open_count == 2


def action() -> None:
    try:
        import subprocess
        subprocess.Popen(
            ["xdg-open", "https://www.google.com"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
    except Exception as exc:
        print(f"[{GESTURE_NAME}] {exc}")