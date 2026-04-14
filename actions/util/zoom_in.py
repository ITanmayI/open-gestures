import subprocess
from actions.base import BaseAction
from actions.system import system

class ZoomIn(BaseAction):
    name = "Zoom In"
    description = "Increase system zoom"
    id = "zoom_in"

    def execute(self) -> None:
        sys = system()

        if sys == "linux":
            try:
                subprocess.Popen(
                    ["ydotool", "key", "29:1", "13:1", "13:0", "29:0"],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                )
            except Exception as exc:
                print(f"[{self.id}] {exc}")

        elif sys == "win":
            try:
                subprocess.Popen(
                    [
                        "powershell", "-Command",
                        "Add-Type -AssemblyName System.Windows.Forms; "
                        "[System.Windows.Forms.SendKeys]::SendWait('^{ADD}')"
                    ],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                )
            except Exception as exc:
                print(f"[{self.id}] {exc}")

        elif sys == "mac":
            # code here
            print("hie")