import math
from collections import deque

# mp landmark ids
TIP_IDS = [4, 8, 12, 16, 20]
PIP_IDS = [2, 6, 10, 14, 18]
WRIST_ID = 0
MIDDLE_MCP_ID = 9


def landmark_distance(a, b):
    return math.hypot(a.x - b.x, a.y - b.y)


def hand_scale(landmarks):
    return landmark_distance(landmarks[WRIST_ID], landmarks[MIDDLE_MCP_ID]) + 1e-6


def get_finger_states(landmarks):
    states = []
    # Thumb heuristic
    states.append(1 if landmarks[TIP_IDS[0]].x > landmarks[PIP_IDS[0]].x else 0)

    # Other fingers
    for tip, pip in zip(TIP_IDS[1:], PIP_IDS[1:]):
        states.append(1 if landmarks[tip].y < landmarks[pip].y else 0)

    return states


def thumb_direction(landmarks):
    tip = landmarks[TIP_IDS[0]]
    wrist = landmarks[WRIST_ID]
    dy = tip.y - wrist.y
    if dy < -0.05:
        return "up"
    if dy > 0.05:
        return "down"
    return "side"


def classify_from_states(landmarks):

    states = tuple(get_finger_states(landmarks))
    tdir = thumb_direction(landmarks)

    if states == (0, 0, 0, 0, 0):
        return "fist"
    if states == (0, 1, 0, 0, 0):
        return "point"
    if states == (0, 1, 1, 0, 0):
        return "peace"
    if states == (1, 1, 1, 1, 1):
        return "open"
    if states[0] == 1 and states[1:] == [0, 0, 0, 0]:
        if tdir == "up":
            return "thumb_up"
        if tdir == "down":
            return "thumb_down"
        return "thumb_side"
    return "unknown"


class StableDetector:
    def __init__(self, window=6):
        self.window = window
        self._dq = deque(maxlen=window)
        self.last_stable = None

    def update(self, value):
        self._dq.append(value)
        if len(self._dq) < self.window:
            return None
        if all(v == self._dq[0] for v in self._dq):
            self.last_stable = self._dq[0]
            return self._dq[0]
        return None