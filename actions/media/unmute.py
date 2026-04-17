import subprocess
from actions.base import BaseAction
from actions.system import system

class UnmuteMedia(BaseAction):
    name = "Unmute Media"
    description = "Unmute system audio"
    id = "unmute_media"

    def execute(self) -> None:
        sys = system()
        if sys == "linux":
            try:
                subprocess.Popen(["playerctl", "volume", "1"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except Exception as exc:
                print(f"[{self.id}] {exc}")
        elif sys == "win":
            print("hi")
        elif sys == "mac":
            try:
                subprocess.Popen(["osascript", "-e", "set volume without output muted"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except Exception as exc:
                print(f"[{self.id}] {exc}")
