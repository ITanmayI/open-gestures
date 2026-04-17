from __future__ import annotations
import time

_defaultCooldowns: dict[str, float] = {
    # ----- Single-hand gestures -----
    "thumb_up_1"    : 0.3,   # volume up
    "thumb_down_1"  : 0.3,   # volume down
    "open_1"        : 0.4,   # play media
    "close_1"       : 0.4,   # pause media
    "point_up_1"    : 0.2,   # brightness up
    "victory_1"     : 0.2,   # brightness down
    "iloveyou_1"    : 1.5,   # mute

    # ----- Double-hand gestures -----
    "thumb_up_2"    : 2.5,   # screenshot
    "thumb_down_2"  : 2.5,   # record screen
    "open_2"        : 4.0,   # open browser
    "close_2"       : 2.0,   # kill active window
    "point_up_2"    : 0.5,   # zoom in
    "victory_2"     : 0.5,   # zoom out
    "iloveyou_2"    : 1.5,   # unmute

    # ----- Motion gestures -----
    "swipe_left"    : 0.6,
    "swipe_right"   : 0.6,
    "swipe_up"      : 0.6,
    "swipe_down"    : 0.6,
}


class Cooldown:
    def __init__(self, overrides: dict[str, float] | None = None) -> None:
        self._durations: dict[str, float] = dict(_defaultCooldowns)  # copy so _defaultCooldowns is never mutated
        if overrides:
            self._durations.update(overrides)
        self._last_trigger: dict[str, float] = {}

    def can_trigger(self, gesture: str) -> bool:
        duration = self._durations.get(gesture, 0.0)  # default value
        if duration == 0.0:
            return True # always allow

        elapsed = time.monotonic() - self._last_trigger.get(gesture, 0.0)
        return elapsed >= duration

    def record(self, gesture: str) -> None:
        self._last_trigger[gesture] = time.monotonic()

    def remaining(self, gesture: str) -> float:
        duration = self._durations.get(gesture, 0.0)
        elapsed  = time.monotonic() - self._last_trigger.get(gesture, 0.0)
        return max(0.0, duration - elapsed)

    def set(self, gesture: str, seconds: float) -> None:
        self._durations[gesture] = seconds