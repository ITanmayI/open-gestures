from __future__ import annotations  # allows 'dict[str, float] | None' syntax on older Python
import time


# Cooldown durations in seconds for every registered gesture.
# Tuned per gesture — double-hand gestures get longer cooldowns since they're
# harder to accidentally hold, single-hand gestures need tighter gates.
_DEFAULTS: dict[str, float] = {
    # ── Single-hand gestures ───────────────────────────────────────────────
    "thumb_up_1"    : 0.3,   # short — volume nudge, fine to repeat quickly
    "thumb_down_1"  : 0.3,
    "open_1"        : 0.4,   # play media
    "close_1"       : 0.4,   # pause media
    "point_up_1"    : 0.2,
    "point_down_1"  : 0.2,
    "iloveyou_1"    : 2.0,   # long — prevents accidental re-trigger

    # ── Double-hand gestures ───────────────────────────────────────────────
    "thumb_up_2"    : 0.8,   # next workspace
    "thumb_down_2"  : 0.8,   # previous workspace
    "open_2"        : 4.0,   # open browser — very long, definitely intentional
    "close_2"       : 0.6,   # kill active window
    "point_up_2"    : 1.0,   # zoom in
    "point_down_2"  : 2.0,   # zoom out — raised because Victory false-triggers easily
    "iloveyou_2"    : 1.0,

    # ── Motion gestures ────────────────────────────────────────────────────
    "swipe_left"    : 0.6,
    "swipe_right"   : 0.6,
    "swipe_up"      : 0.6,
    "swipe_down"    : 0.6,
}


class Cooldown:
    def __init__(self, overrides: dict[str, float] | None = None) -> None:
        self._durations: dict[str, float] = dict(_DEFAULTS)  # copy so _DEFAULTS is never mutated
        if overrides:
            self._durations.update(overrides)  # allow per-instance overrides at construction time
        self._last_trigger: dict[str, float] = {}  # maps gesture name → last trigger timestamp

    def can_trigger(self, gesture: str) -> bool:
        """
        Returns True if enough time has passed since this gesture last fired.
        Fail-open: gestures not in _DEFAULTS always return True so new modules
        don't silently break before they're added here.
        """
        duration = self._durations.get(gesture, 0.0)  # 0.0 = not registered = no cooldown
        if duration == 0.0:
            return True  # unregistered gesture — always allow

        elapsed = time.monotonic() - self._last_trigger.get(gesture, 0.0)
        # _last_trigger.get(gesture, 0.0) returns 0.0 if never triggered,
        # so elapsed will be huge and can_trigger returns True on first call
        return elapsed >= duration

    def record(self, gesture: str) -> None:
        """Stamp the current time as the last trigger for this gesture."""
        self._last_trigger[gesture] = time.monotonic()

    def remaining(self, gesture: str) -> float:
        """
        How many seconds until this gesture is ready to fire again.
        Returns 0.0 if already ready. Useful for debug overlays.
        """
        duration = self._durations.get(gesture, 0.0)
        elapsed  = time.monotonic() - self._last_trigger.get(gesture, 0.0)
        return max(0.0, duration - elapsed)

    def set(self, gesture: str, seconds: float) -> None:
        """Override a cooldown duration at runtime without restarting."""
        self._durations[gesture] = seconds