import subprocess
from actions.base import BaseAction
from actions.system import system

class OpenBrowser(BaseAction):
    name = "Open Browser"
    description = "Open the default browser"
    id = "open_browser"

    def execute(self) -> None:
        sys = system()
        
        if sys=="linux":
            try:
                subprocess.Popen(
                    ["xdg-open", "https://www.google.com"],
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