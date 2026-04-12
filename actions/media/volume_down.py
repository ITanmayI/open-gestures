import subprocess
from actions.base import BaseAction
from actions.system import system

class VolumeDown(BaseAction):
    name = "Volume Down"
    description = "Decrease system volume"
    id = "volume_down"

    def execute(self) -> None:
        sys = system()
        
        if sys=="linux":
            try:
                subprocess.Popen(
                    ["pactl", "set-sink-volume", "@DEFAULT_SINK@", "-5%"],
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
