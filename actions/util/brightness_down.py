import subprocess
from actions.base import BaseAction
from actions.system import system

class BrightnessDown(BaseAction):
    name = "Brightness Down"
    description = "Reduce system brightness"
    id = "brightness_down"

    def execute(self) -> None:
        sys = system()
        
        if sys=="linux":
                try:
                    import subprocess
                    subprocess.Popen(
                        ["brightnessctl", "set", "5%-"],
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
