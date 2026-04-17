import subprocess
from actions.base import BaseAction
from actions.system import system

class ZoomOut(BaseAction):
    name = "Zoom Out"
    description = "Decrease system zoom"
    id = "zoom_out"

    def execute(self) -> None:
        sys = system()

        if sys == "linux":
            try:
                subprocess.Popen(
                    ["ydotool", "key", "29:1", "12:1", "12:0", "29:0"],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                )
            except Exception as exc:
                print(f"[{self.id}] {exc}")

        elif sys == "win":
            # Ctrl + Minus via PowerShell SendKeys
            try:
                subprocess.Popen(
                    [
                        "powershell", "-Command",
                        "Add-Type -AssemblyName System.Windows.Forms; "
                        "[System.Windows.Forms.SendKeys]::SendWait('^{SUBTRACT}')"
                    ],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                )
            except Exception as exc:
                print(f"[{self.id}] {exc}")

        elif sys == "mac":
            try:
                subprocess.Popen(["osascript", "-e", "tell application \"System Events\" to keystroke \"-\" using command down"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except Exception as exc:
                print(f"[{self.id}] {exc}")
