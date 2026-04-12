import subprocess
from actions.base import BaseAction
from actions.system import system

class MuteMedia(BaseAction):
    name = "Mute Media"
    description = "Mute system media"
    id = "mute_media"

    def execute(self) -> None:
        sys = system()
        
        if sys=="linux":
                try:
                    subprocess.Popen(
                        ["pactl", "set-sink-mute", "@DEFAULT_SINK@", "1"],
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
