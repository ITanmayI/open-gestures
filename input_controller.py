import shutil
import subprocess
import os
import json

WAYLAND = bool(os.environ.get("WAYLAND_DISPLAY") or os.environ.get("XDG_SESSION_TYPE") == "wayland")
BACKEND = "noop"

if WAYLAND and shutil.which("ydotool"):
    BACKEND = "ydotool"
elif not WAYLAND and shutil.which("xdotool"):
    BACKEND = "xdotool"
else:
    BACKEND = "noop"


def run_quiet(cmd):
    try:
        subprocess.run(cmd, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except Exception:
        return False


# Media controls
def play_pause():
    if shutil.which("playerctl"):
        run_quiet(["playerctl", "play-pause"])
        return
    if BACKEND == "ydotool":
        run_quiet(["ydotool", "key", "KEY_PLAYPAUSE"])
        return
    if BACKEND == "xdotool":
        run_quiet(["xdotool", "key", "XF86AudioPlay"])
        return
    print("[INPUT noop] play_pause")


# Volume controls
def volume_change(delta_percent):
    if shutil.which("pactl"):
        sign = "+" if delta_percent > 0 else "-"
        amt = abs(delta_percent)
        run_quiet(["pactl", "set-sink-volume", "@DEFAULT_SINK@", f"{amt}%{sign}"])
        return

    if BACKEND == "ydotool":
        key = "KEY_VOLUMEUP" if delta_percent > 0 else "KEY_VOLUMEDOWN"
        run_quiet(["ydotool", "key", key])
        return

    if BACKEND == "xdotool":
        key = "XF86AudioRaiseVolume" if delta_percent > 0 else "XF86AudioLowerVolume"
        run_quiet(["xdotool", "key", key])
        return
    print(f"[INPUT noop] volume_change {delta_percent}%")


def toggle_mute():
    if shutil.which("pactl"):
        run_quiet(["pactl", "set-sink-mute", "@DEFAULT_SINK@", "toggle"])
        return

    if BACKEND in ("ydotool", "xdotool"):
        key = "KEY_MUTE" if BACKEND == "ydotool" else "XF86AudioMute"
        run_quiet([BACKEND.replace("ydotool", "ydotool").replace("xdotool", "xdotool"), "key", key])
        return
    print("[INPUT noop] toggle_mute")


# Brightness controls
def brightness_change(delta_percent):
    if shutil.which("brightnessctl"):
        sign = "+" if delta_percent > 0 else "-"
        amt = abs(delta_percent)
        run_quiet(["brightnessctl", "set", f"{amt}%{sign}"])
        return
    if shutil.which("light"):
        sign = "+" if delta_percent > 0 else "-"
        amt = abs(delta_percent)
        run_quiet(["light", "-S", f"{amt}%{sign}"])
        return
    print(f"[INPUT noop] brightness_change {delta_percent}%")