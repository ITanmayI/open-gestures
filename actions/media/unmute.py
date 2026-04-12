import subprocess
from actions.base import BaseAction
from actions.system import system

class UnmuteMedia(BaseAction):
    name = "Unmute"
    description = "Unmute system media"
    id = "unmute_media"

    def execute(self) -> None:
        sys = system()
        
        if sys=="linux":
            try:
                subprocess.Popen(
                    ["pactl", "set-sink-mute", "@DEFAULT_SINK@", "0"], 
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                )
            except Exception as exc:
                print(f"[{self.id}] {exc}")
        elif sys=="win":
            #code here
            print("hi")
        elif sys=="mac":
            #code here
            print("hie")
