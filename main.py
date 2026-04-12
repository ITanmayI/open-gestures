from __future__ import annotations

import os
import time
import threading
from pathlib import Path

import cv2
import mediapipe as mp
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision as mp_vision
from mediapipe.tasks.python.vision.core.vision_task_running_mode import VisionTaskRunningMode

from core.cooldown import Cooldown
from core.router  import GestureRouter

# Forces OpenCV to use X11/xcb backend on Wayland — without this cv2.imshow() can crash
os.environ.setdefault("QT_QPA_PLATFORM", "xcb")

MODEL_PATH = Path(__file__).parent / "models" / "gesture_recognizer.task"


# ── Thread-safe result slot ────────────────────────────────────────────────

class _ResultSlot:
    """Passes MediaPipe results from its callback thread to the main loop safely."""

    def __init__(self) -> None:
        self._lock   = threading.Lock()
        self._result = None
        self._label  = ""

    def put(self, result) -> None:
        with self._lock:
            self._result = result
            self._label  = _format_label(result)

    def get(self):
        with self._lock:
            return self._result

    def label(self) -> str:
        with self._lock:
            return self._label


def _format_label(result) -> str:
    """Converts a GestureRecognizerResult into a readable string for the overlay."""
    if not result or not result.gestures:
        return ""
    parts = []
    for i, hand_gestures in enumerate(result.gestures):
        if hand_gestures:
            top  = hand_gestures[0]
            side = ""
            if result.handedness and i < len(result.handedness):
                side = result.handedness[i][0].category_name + " "
            parts.append(f"{side}{top.category_name} ({top.score:.2f})")
    return "  |  ".join(parts)


# ── MediaPipe recognizer ───────────────────────────────────────────────────

def _build_recognizer(slot: _ResultSlot) -> mp_vision.GestureRecognizer:
    def _on_result(result, _output_image, _timestamp_ms: int) -> None:
        slot.put(result)  # store only — never draw from a callback thread

    options = mp_vision.GestureRecognizerOptions(
        base_options=mp_python.BaseOptions(model_asset_path=str(MODEL_PATH)),
        running_mode=VisionTaskRunningMode.LIVE_STREAM,
        num_hands=2,
        min_hand_detection_confidence=0.5,
        min_hand_presence_confidence=0.5,
        min_tracking_confidence=0.5,
        result_callback=_on_result,
    )
    return mp_vision.GestureRecognizer.create_from_options(options)


# ── Overlay ────────────────────────────────────────────────────────────────

def _draw_overlay(frame, label: str, fired: str) -> None:
    h, w = frame.shape[:2]
    bar  = frame.copy()
    cv2.rectangle(bar, (0, 0), (w, 60), (0, 0, 0), -1)
    cv2.addWeighted(bar, 0.45, frame, 0.55, 0, frame)
    cv2.putText(frame, f"Detected: {label or 'none'}",
                (12, 24), cv2.FONT_HERSHEY_SIMPLEX, 0.60, (200, 230, 255), 1, cv2.LINE_AA)
    if fired:
        cv2.putText(frame, f"Action fired: {fired}",
                    (12, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.60, (80, 255, 120), 2, cv2.LINE_AA)


# ── Main ───────────────────────────────────────────────────────────────────

def main() -> None:
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model not found: {MODEL_PATH}\n"
            "Download with:\n"
            "  wget https://storage.googleapis.com/mediapipe-models/"
            "gesture_recognizer/gesture_recognizer/float16/latest/"
            "gesture_recognizer.task -O models/gesture_recognizer.task"
        )

    slot   = _ResultSlot()
    router = GestureRouter(Cooldown())  # router loads gestures + actions internally

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
    if not cap.isOpened():
        raise RuntimeError("Cannot open webcam at index 0.")

    cap.set(cv2.CAP_PROP_FRAME_WIDTH,  640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 30)

    recognizer = _build_recognizer(slot)

    t0               = time.monotonic()
    last_ts          = -1
    fired_name       = ""
    fired_clear_time = 0.0

    print("Open-Gestures running. Press ESC to exit.")

    try:
        while True:
            ret, bgr = cap.read()
            if not ret:
                time.sleep(0.01)
                continue

            bgr = cv2.flip(bgr, 1)
            rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)

            ts_ms = int((time.monotonic() - t0) * 1000)
            if ts_ms <= last_ts:
                ts_ms = last_ts + 1
            last_ts = ts_ms

            # .copy() required — MediaPipe holds a buffer reference across threads
            recognizer.recognize_async(
                mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb.copy()),
                ts_ms,
            )

            result    = slot.get()
            triggered = router.route(result)
            now       = time.monotonic()

            if triggered:
                fired_name       = triggered
                fired_clear_time = now + 1.2
            if now >= fired_clear_time:
                fired_name = ""

            _draw_overlay(bgr, slot.label(), fired_name)
            cv2.imshow("Open-Gestures", bgr)

            if cv2.waitKey(1) & 0xFF == 27:
                break

    finally:
        cap.release()
        recognizer.close()
        cv2.destroyAllWindows()
        print("Exited cleanly.")


if __name__ == "__main__":
    main()