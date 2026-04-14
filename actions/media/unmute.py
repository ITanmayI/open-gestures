import subprocess
from actions.base import BaseAction
from actions.system import system
 
class UnmuteMedia(BaseAction):
    name = "Unmute"
    description = "Unmute system media"
    id = "unmute_media"
 
    def execute(self) -> None:
        sys = system()
 
        if sys == "linux":
            try:
                subprocess.Popen(
                    ["pactl", "set-sink-mute", "@DEFAULT_SINK@", "0"],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                )
            except Exception as exc:
                print(f"[{self.id}] {exc}")
 
        elif sys in ("win", "windows"):
            try:
                import pythoncom
                from ctypes import cast, POINTER
                from comtypes import CLSCTX_ALL
                from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
                pythoncom.CoInitialize()
                try:
                    devices = AudioUtilities.GetSpeakers()
                    interface = devices._dev.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                    volume = cast(interface, POINTER(IAudioEndpointVolume))
                    volume.SetMute(0, None)
                finally:
                    pythoncom.CoUninitialize()
            except Exception as exc:
                print(f"[{self.id}] {exc}")
        elif sys=="mac":
            #code here
            print("hie")
