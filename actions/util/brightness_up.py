import subprocess
from actions.base import BaseAction
from actions.system import system
 
class BrightnessUp(BaseAction):
    name = "Brightness Up"
    description = "Increase system brightness"
    id = "brightness_up"
 
    def execute(self) -> None:
        sys = system()
 
        if sys == "linux":
            try:
                subprocess.Popen(
                    ["brightnessctl", "set", "5%+"],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                )
            except Exception as exc:
                print(f"[{self.id}] {exc}")
 
        elif sys in ("win", "windows"):
            try:
                import screen_brightness_control as sbc
                current = sbc.get_brightness(display=0)[0]
                sbc.set_brightness(min(100, current + 5))
            except Exception as exc:
                print(f"[{self.id}] {exc}")
                
        elif sys=="mac":
            #code here
            print("hie")
