# open-gestures

Open-source, real-time hand gesture control for **all major operating systems** using MediaPipe and OpenCV. The system reads frames from a webcam, classifies hand gestures using a MediaPipe GestureRecognizer model running in live-stream mode, and routes recognized gestures to modular action handlers. Up to two hands are tracked simultaneously, with priority given to two-hand gestures over single-hand ones.

---

## Working Gestures

#### Single Hand                    Dual Hand

<table>
<tr>
<td valign="top">

<table>
<tr><th>S. No</th><th>Gesture Name</th></tr>
<tr><td>1. 👍</td><td>Thumb up</td></tr>
<tr><td>2. 👎</td><td>Thumb down</td></tr>
<tr><td>3. ✌️</td><td>Victory</td></tr>
<tr><td>4. ☝️</td><td>Point up</td></tr>
<tr><td>5. ✊</td><td>Closed</td></tr>
<tr><td>6. 🖐️</td><td>Open</td></tr>
<tr><td>7. 🤟</td><td>I Love You</td></tr>
</table>

</td>
<td valign="top">

<table>
<tr><th>S. No</th><th>Gesture Name</th></tr>
<tr><td>1. 👍👍</td><td>Thumb up 2</td></tr>
<tr><td>2. 👎👎</td><td>Thumb down 2</td></tr>
<tr><td>3. ✌️✌️</td><td>Victory 2</td></tr>
<tr><td>4. ☝️☝️</td><td>Point up 2</td></tr>
<tr><td>5. ✊✊</td><td>Closed 2</td></tr>
<tr><td>6. 🖐️🖐️</td><td>Open 2</td></tr>
<tr><td>7. 🤟🤟</td><td>I Love You 2</td></tr>
</table>

</td>
</tr>
</table>

---

## How It Works

A webcam feed is captured frame by frame using OpenCV. Each frame is converted from BGR to RGB and passed asynchronously to MediaPipe's GestureRecognizer, which runs on an internal thread. Results are stored in a thread-safe slot and consumed on the main loop. The latest available result is passed to a `GestureRouter`, which checks every registered gesture module in priority order. If a module's `matches()` function returns true and its cooldown has elapsed, the module's `action()` is executed. An overlay is drawn on the current frame showing the detected gesture label and the last fired action, then displayed in an OpenCV window.

The system uses `LIVE_STREAM` mode from the MediaPipe Tasks API, which means `recognize_async()` returns immediately and results arrive via a callback on a separate thread. A `threading.Lock` is used to safely pass results from the callback thread to the main loop.

---

## Project Structure

```
open-gestures/
├── main.py                  Entry point. Runs the camera loop, recognizer, and router.
├── models/
│   └── gesture_recognizer.task   MediaPipe model file.
├── core/
│   └── cooldown.py          Cooldown manager preventing gesture actions from firing too rapidly.
│   └── router.py            Router for linking actions with gestures
└── gestures/
    ├── static/              Gesture modules that match on a single static hand pose.
    └── motion/              Gesture modules that match on motion-based or temporal gestures. (Work In Progress)
```

Each file under `gestures/static/` and `gestures/motion/` is a self-contained Python module. Modules ending in `_2` represent two-hand gestures and are loaded with higher priority than single-hand (`_1`) modules.

---

## Gesture Module Contract

Every gesture module must expose two things:

```python
GESTURE_NAME: str       # Unique identifier used as the cooldown key and display label.

def matches(result) -> bool:
    # Receives a MediaPipe GestureRecognizerResult.
    # Return True if this gesture should fire given the current result.
```

Modules that do not expose all two attributes are skipped at load time with a warning.

---

## Action Module Contract

Every action module must expose four things:

```python
ACTION_NAME: str         # Unique identifier used as the cooldown key and display label.
ACTION_DESCRIPTION: str  # Unique description shown in the GUI.
ACTION_ID: str           # Unique ID used by the router to connect gestures with the action.

def execute(self) -> None:
    # Action logic here.
```

Modules that do not expose all four attributes are skipped at load time with a warning.

---

## Requirements

**Operating System:** Linux / Windows / macOS

**Python:** 3.9 or later is recommended for compatibility with the MediaPipe Tasks API.

**Hardware:** An accessible webcam.

**Dependencies:**

| Package | Purpose |
|---|---|
| `mediapipe` | Hand landmark detection and gesture classification via the Tasks API |
| `opencv-python` | Webcam capture, frame processing, and display window |
| `numpy` | Implicit dependency of both mediapipe and opencv |

---

## Installation

**1. Clone the repository**

```bash
git clone https://github.com/GodKode69/open-gestures.git
cd open-gestures
```

**2. Create and activate a virtual environment (recommended)**

On Linux / macOS:
```bash
python3 -m venv env
source env/bin/activate
```

On Windows:
```bash
python -m venv env
env\Scripts\activate
```

**3. Install Python dependencies**

```bash
pip install mediapipe opencv-python numpy
```

**4. Download the MediaPipe model**

The gesture recognizer model must be downloaded separately and placed at `models/gesture_recognizer.task`. You can obtain it from [Google's MediaPipe model page](https://developers.google.com/mediapipe/solutions/vision/gesture_recognizer).

---

## Running

```bash
python main.py
```

The application will open a window titled `Open-Gestures` showing the gestures with their bound actions, with the option to switch actions and also to reset them to defaults. A preview option is also available to preview your webcam with gesture and action detection.

---

## Cooldown System

The `Cooldown` class in `core/cooldown.py` prevents a gesture action from firing multiple times in rapid succession. Each gesture module is gated by its `GESTURE_NAME` key. When a gesture fires, its timestamp is recorded and subsequent triggers are blocked until the cooldown period elapses. This prevents unintended repeated actions from a held or slowly-changing pose.

---

## Recognizer Configuration

The recognizer is configured with the following defaults in `main.py`:

| Parameter | Value |
|---|---|
| `num_hands` | 2 |
| `min_hand_detection_confidence` | 0.5 |
| `min_hand_presence_confidence` | 0.5 |
| `min_tracking_confidence` | 0.5 |
| Camera resolution | 640 × 480 |
| Camera target FPS | 30 |

These values can be adjusted directly in `main.py` inside the `build_recognizer` function and the `cap.set(...)` calls in `main()`.

---

## Technologies Used

**Python** — Primary implementation language.

**MediaPipe (Tasks API)** — Google's framework for on-device ML pipelines. Specifically, `mediapipe.tasks.python.vision.GestureRecognizer` is used in `LIVE_STREAM` mode with an asynchronous result callback. The underlying model classifies hand gestures from landmark data.

**MediaPipe GestureRecognizer model (`gesture_recognizer.task`)** — A float16 TFLite model that performs hand detection, landmark estimation, and gesture classification in a single pipeline. Downloaded separately from Google's model storage.

**OpenCV (`cv2`)** — Used for webcam capture via `VideoCapture`, frame color conversion, mirror flipping, text and rectangle overlays, and the display window.

**Python `threading` module** — Used to safely transfer `GestureRecognizerResult` objects from MediaPipe's internal callback thread to the main loop via a `threading.Lock`.

**Python `importlib` and `pkgutil`** — Used for dynamic discovery and loading of gesture modules at runtime without any hard-coded imports.

---

## Contributing

Contributions are welcome! If you'd like to add new gesture modules, action handlers, or platform support, feel free to open a pull request on the [GitHub repository](https://github.com/GodKode69/open-gestures/tree/main).

---

## License

All rights are reserved by the author and the contributors.
