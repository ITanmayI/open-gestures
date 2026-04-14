import subprocess
from actions.base import BaseAction
from actions.system import system
 
class VolumeUp(BaseAction):
    name = "Volume Up"
    description = "Increase system volume"
    id = "volume_up"
 
    def execute(self) -> None:
        sys = system()
 
        if sys == "linux":
            try:
                subprocess.Popen(
                    ["pactl", "set-sink-volume", "@DEFAULT_SINK@", "+5%"],
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
                    current = volume.GetMasterVolumeLevelScalar()
                    volume.SetMasterVolumeLevelScalar(min(1.0, current + 0.05), None)
                finally:
                    pythoncom.CoUninitialize()
            except Exception as exc:
                print(f"[{self.id}] {exc}")
        elif sys=="mac":
            #code here
            print("hie")
