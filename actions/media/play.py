import subprocess
from actions.base import BaseAction
from actions.system import system
 
class PlayMedia(BaseAction):
    name = "Play Media"
    description = "Play system media"
    id = "play_media"
 
    def execute(self) -> None:
        sys = system()
 
        if sys == "linux":
            try:
                subprocess.Popen(
                    ["playerctl", "play"],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                )
            except Exception as exc:
                print(f"[{self.id}] {exc}")
 
        elif sys in ("win", "windows"):
            try:
                from pynput.keyboard import Key, Controller
                kb = Controller()
                kb.press(Key.media_play_pause)
                kb.release(Key.media_play_pause)
            except Exception as exc:
                print(f"[{self.id}] {exc}")
        elif sys=="mac":
            try:
                subprocess.Popen(
                    ["osascript", "-e", "tell application \"System Events\" to key code 16"],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                )
            except Exception as exc:
                print(f"[{self.id}] {exc}")