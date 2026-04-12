import subprocess
from actions.base import BaseAction
from actions.system import system

class VolumeUp(BaseAction):
    name = "Volume Up"
    description = "Increase system volume"
    id = "volume_up"

    def execute(self) -> None:
        sys = system()
        
        if sys=="linux":
            try:
                subprocess.Popen(
                    ["pactl", "set-sink-volume", "@DEFAULT_SINK@", "+5%"],
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
