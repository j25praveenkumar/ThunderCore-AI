"""
Thunder AI — Windows Automation Engine
Handles system commands, app control, browser, file management, volume.
"""
import os
import subprocess
import webbrowser
import logging
import re
from typing import Tuple

logger = logging.getLogger(__name__)

# ── Default app paths (user can extend via DB) ────────────────────────────────
DEFAULT_APPS = {
    "chrome":    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "edge":      r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    "vscode":    r"C:\Users\{user}\AppData\Local\Programs\Microsoft VS Code\Code.exe",
    "notepad":   "notepad.exe",
    "calculator":"calc.exe",
    "explorer":  "explorer.exe",
    "cmd":       "cmd.exe",
    "settings":  "ms-settings:",
    "control":   "control.exe",
    "task manager": "taskmgr.exe",
}


def _run(cmd: list) -> Tuple[bool, str]:
    try:
        subprocess.Popen(cmd, shell=True)
        return True, "Done"
    except Exception as e:
        logger.error(f"Command failed: {e}")
        return False, str(e)


# ── System ────────────────────────────────────────────────────────────────────
def shutdown_pc(delay: int = 10) -> str:
    os.system(f"shutdown /s /t {delay}")
    return f"PC will shut down in {delay} seconds."

def restart_pc(delay: int = 10) -> str:
    os.system(f"shutdown /r /t {delay}")
    return f"PC will restart in {delay} seconds."

def lock_pc() -> str:
    os.system("rundll32.exe user32.dll,LockWorkStation")
    return "PC locked."

def sleep_pc() -> str:
    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
    return "Going to sleep..."

def cancel_shutdown() -> str:
    os.system("shutdown /a")
    return "Shutdown/restart cancelled."


# ── Volume ────────────────────────────────────────────────────────────────────
def volume_up() -> str:
    # Uses NirCmd if available, else fallback PowerShell
    try:
        from ctypes import cast, POINTER
        from comtypes import CLSCTX_ALL
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        current = volume.GetMasterVolumeLevelScalar()
        volume.SetMasterVolumeLevelScalar(min(1.0, current + 0.1), None)
        return f"Volume increased to {int(min(1.0, current + 0.1) * 100)}%"
    except Exception:
        subprocess.run(["powershell", "-c",
            "(New-Object -comObject WScript.Shell).SendKeys([char]175)"], shell=True)
        return "Volume increased."

def volume_down() -> str:
    try:
        from ctypes import cast, POINTER
        from comtypes import CLSCTX_ALL
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        current = volume.GetMasterVolumeLevelScalar()
        volume.SetMasterVolumeLevelScalar(max(0.0, current - 0.1), None)
        return f"Volume decreased to {int(max(0.0, current - 0.1) * 100)}%"
    except Exception:
        subprocess.run(["powershell", "-c",
            "(New-Object -comObject WScript.Shell).SendKeys([char]174)"], shell=True)
        return "Volume decreased."

def mute_volume() -> str:
    subprocess.run(["powershell", "-c",
        "(New-Object -comObject WScript.Shell).SendKeys([char]173)"], shell=True)
    return "Volume muted/unmuted."


# ── Applications ──────────────────────────────────────────────────────────────
def open_app(app_name: str) -> str:
    name = app_name.lower().strip()
    path = DEFAULT_APPS.get(name)
    if path:
        try:
            if path.startswith("ms-"):
                os.startfile(path)
            else:
                subprocess.Popen(path, shell=True)
            return f"Opening {app_name}..."
        except Exception as e:
            return f"Failed to open {app_name}: {e}"
    # Fallback: try to run as-is
    try:
        subprocess.Popen(app_name, shell=True)
        return f"Trying to open {app_name}..."
    except Exception as e:
        return f"Could not open {app_name}: {e}"

def close_app(process_name: str) -> str:
    try:
        os.system(f"taskkill /f /im {process_name}.exe")
        return f"Closed {process_name}."
    except Exception as e:
        return f"Failed to close {process_name}: {e}"


# ── Browser ───────────────────────────────────────────────────────────────────
def open_website(url: str) -> str:
    if not url.startswith("http"):
        url = "https://" + url
    webbrowser.open(url)
    return f"Opening {url} in browser."

def search_google(query: str) -> str:
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    webbrowser.open(url)
    return f"Searching Google for: {query}"

def search_youtube(query: str) -> str:
    url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
    webbrowser.open(url)
    return f"Searching YouTube for: {query}"


# ── File / Folder ─────────────────────────────────────────────────────────────
def create_folder(path: str) -> str:
    try:
        os.makedirs(path, exist_ok=True)
        return f"Folder created: {path}"
    except Exception as e:
        return f"Failed to create folder: {e}"

def delete_path(path: str) -> str:
    try:
        if os.path.isfile(path):
            os.remove(path)
            return f"File deleted: {path}"
        elif os.path.isdir(path):
            import shutil
            shutil.rmtree(path)
            return f"Folder deleted: {path}"
        else:
            return f"Path not found: {path}"
    except Exception as e:
        return f"Delete failed: {e}"

def list_folder(path: str = ".") -> str:
    try:
        items = os.listdir(path)
        return "\n".join(items) if items else "Empty folder."
    except Exception as e:
        return f"Error: {e}"
