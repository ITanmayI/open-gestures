import subprocess
from actions.base import BaseAction
from actions.system import system
import json

with open('data/config.json', 'r') as file:
    data = json.load(file)

wm_config = data["config"]["window_manager"]
window_manager = wm_config.get("custom") or wm_config.get("default")

class CloseWindow(BaseAction):
    name = "Close Window"
    description = "Close active window"
    id = "close_window"

    def execute(self) -> None:
        sys = system()

        if sys == "linux":
            if window_manager == "hyprland":
                try:
                    subprocess.Popen(
                        ["hyprctl", "dispatch", "killactive"],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                    )
                except Exception as exc:
                    print(f"[{self.id}] {exc}")

        elif sys == "win":
            # Send Alt+F4 to gracefully close the active window
            try:
                subprocess.Popen(
                    [
                        "powershell", "-Command",
                        "Add-Type -AssemblyName System.Windows.Forms; "
                        "[System.Windows.Forms.SendKeys]::SendWait('%{F4}')"
                    ],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                )
            except Exception as exc:
                print(f"[{self.id}] {exc}")

        elif sys == "mac":
            try:
                subprocess.Popen(["osascript", "-e", "tell application \"System Events\" to keystroke \"w\" using command down"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except Exception as exc:
                print(f"[{self.id}] {exc}")
