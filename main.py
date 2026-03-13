import time
import cv2
import mediapipe as mp
from gestures import classify_from_states, StableDetector, hand_scale
import input_controller as ic

# mp api
BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode
    
MODEL = "hand_landmarker.task" 

gesture_stable = StableDetector(window=6)

# seconds
COOLDOWNS = {
    "play_pause": 1.0,
    "mute": 1.0,
    "volume": 0.20,
    "brightness": 0.20,
    "workspace": 0.6
}
last_trigger = {k: 0.0 for k in COOLDOWNS.keys()}


def now():
    return time.monotonic()

def can_trigger(action):
    t = now()
    if t - last_trigger[action] >= COOLDOWNS[action]:
        last_trigger[action] = t
        return True
    return False


def map_and_trigger(gesture, landmarks):
    """
    - fist        -> play/pause
    - point       -> brightness down
    - peace       -> brightness up
    - thumb_up    -> volume up (repeatable)
    - thumb_down  -> volume down (repeatable)
    - open        -> toggle mute
    """
    if gesture == "fist":
        if can_trigger("play_pause"):
            ic.play_pause()
            print("[ACTION] play_pause")

    elif gesture == "point":
        if can_trigger("brightness"):
            ic.brightness_change(-5)
            print("[ACTION] brightness -5%")

    elif gesture == "peace":
        if can_trigger("brightness"):
            ic.brightness_change(+5)
            print("[ACTION] brightness +5%")

    elif gesture == "thumb_up":
        if can_trigger("volume"):
            ic.volume_change(+5)
            print("[ACTION] volume +5%")

    elif gesture == "thumb_down":
        if can_trigger("volume"):
            ic.volume_change(-5)
            print("[ACTION] volume -5%")

    elif gesture == "open":
        if can_trigger("play_pause"):
            ic.play_pause()
            print("[ACTION] play_pause")

    # unknown 


def main():
    options = HandLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=MODEL),
        running_mode=VisionRunningMode.VIDEO,
        num_hands=1,
        min_hand_detection_confidence=0.5,
        min_hand_presence_confidence=0.5,
        min_tracking_confidence=0.5
    )

    cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
    if not cap.isOpened():
        print("ERROR: cannot open camera")
        return

    with HandLandmarker.create_from_options(options) as landmarker:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)  
            h, w, _ = frame.shape
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
            ts = int(cap.get(cv2.CAP_PROP_POS_MSEC))
            if ts <= 0:
                ts = int(now() * 1000)

            result = landmarker.detect_for_video(mp_image, ts)

            gesture_label = "none"
            if result.hand_landmarks:
                hand_landmarks = result.hand_landmarks[0]

                for lm in hand_landmarks:
                    x = int(lm.x * w)
                    y = int(lm.y * h)
                    cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)

                gesture = classify_from_states(hand_landmarks)
                stable = gesture_stable.update(gesture)
                if stable:
                    scale = hand_scale(hand_landmarks)
                    map_and_trigger(stable, hand_landmarks)
                    gesture_label = stable
                else:
                    gesture_label = gesture

            cv2.putText(frame, f"Gesture: {gesture_label}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
            cv2.imshow("Gesture Controls", frame)

            if cv2.waitKey(1) & 0xFF == 27:
                break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()