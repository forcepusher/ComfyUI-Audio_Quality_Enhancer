"""
SoX binary management for ComfyUI-SlopAudio.
Embeds SoX within the extension directory. Auto-downloads on Windows if missing.
"""

import os
import platform
import shutil
import subprocess
import zipfile
import urllib.request

SOX_VERSION = "14.4.2"
SOX_WIN_ZIP = f"sox-{SOX_VERSION}-win32.zip"
SOX_WIN_DIR = f"sox-{SOX_VERSION}"
SOX_WIN_URL = (
    f"https://sourceforge.net/projects/sox/files/sox/{SOX_VERSION}/{SOX_WIN_ZIP}/download"
)

_EXTENSION_DIR = os.path.dirname(os.path.abspath(__file__))
_BIN_DIR = os.path.join(_EXTENSION_DIR, "bin")

_cached_sox_path: str | None = None


def _find_embedded_sox() -> str | None:
    """Look for SoX in the embedded bin/ directory."""
    if platform.system() == "Windows":
        candidate = os.path.join(_BIN_DIR, SOX_WIN_DIR, "sox.exe")
    else:
        candidate = os.path.join(_BIN_DIR, "sox")

    if os.path.isfile(candidate):
        return candidate
    return None


def _find_system_sox() -> str | None:
    """Look for SoX on the system PATH or well-known install locations."""
    found = shutil.which("sox")
    if found:
        return found

    if platform.system() == "Windows":
        candidates = [
            rf"C:\Program Files (x86)\sox-14-4-2\sox.exe",
            rf"C:\Program Files\sox-14-4-2\sox.exe",
            rf"C:\Program Files (x86)\sox-14.4.2\sox.exe",
            rf"C:\Program Files\sox-14.4.2\sox.exe",
            rf"C:\Program Files (x86)\sox\sox.exe",
            rf"C:\Program Files\sox\sox.exe",
        ]
    else:
        candidates = ["/usr/bin/sox", "/usr/local/bin/sox", "/bin/sox"]

    for path in candidates:
        if os.path.isfile(path) and os.access(path, os.X_OK):
            return path

    return None


def download_sox(force: bool = False) -> bool:
    """Download and extract SoX into the embedded bin/ directory.

    Currently only auto-downloads on Windows (portable zip).
    Linux/macOS users should install SoX via their package manager.

    Returns True on success.
    """
    if platform.system() != "Windows":
        print("[SoX] Auto-download is only supported on Windows.")
        print("[SoX] On Linux, install via:  sudo apt-get install sox")
        print("[SoX] On macOS, install via:  brew install sox")
        return False

    sox_exe = os.path.join(_BIN_DIR, SOX_WIN_DIR, "sox.exe")
    if os.path.isfile(sox_exe) and not force:
        print(f"[SoX] Already installed at {sox_exe}")
        return True

    os.makedirs(_BIN_DIR, exist_ok=True)
    zip_path = os.path.join(_BIN_DIR, SOX_WIN_ZIP)

    print(f"[SoX] Downloading SoX {SOX_VERSION} for Windows ...")
    try:
        urllib.request.urlretrieve(SOX_WIN_URL, zip_path)
    except Exception as e:
        print(f"[SoX] Download failed: {e}")
        return False

    print(f"[SoX] Extracting to {_BIN_DIR} ...")
    try:
        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(_BIN_DIR)
    except Exception as e:
        print(f"[SoX] Extraction failed: {e}")
        return False
    finally:
        try:
            os.remove(zip_path)
        except OSError:
            pass

    if os.path.isfile(sox_exe):
        print(f"[SoX] Successfully installed at {sox_exe}")
        return True

    print(f"[SoX] Installation failed — {sox_exe} not found after extraction")
    return False


def get_sox_executable() -> str | None:
    """Return the path to a usable SoX executable.

    Resolution order:
      1. Embedded binary in ``<extension>/bin/``
      2. System PATH / well-known install locations
      3. Auto-download (Windows only)

    The result is cached after the first successful lookup.
    """
    global _cached_sox_path
    if _cached_sox_path and os.path.isfile(_cached_sox_path):
        return _cached_sox_path

    sox = _find_embedded_sox()
    if not sox:
        sox = _find_system_sox()
    if not sox and platform.system() == "Windows":
        print("[SoX] Not found locally. Attempting auto-download ...")
        if download_sox():
            sox = _find_embedded_sox()

    if sox:
        _cached_sox_path = sox
    return sox


def ensure_sox() -> str:
    """Return the SoX path or raise with platform-specific install instructions."""
    sox = get_sox_executable()
    if sox:
        return sox

    system = platform.system()
    if system == "Windows":
        raise RuntimeError(
            "SoX not found and auto-download failed. "
            "Please download SoX manually from "
            f"https://sourceforge.net/projects/sox/files/sox/{SOX_VERSION}/ "
            f"and extract it to: {os.path.join(_BIN_DIR, SOX_WIN_DIR)}"
        )
    elif system == "Darwin":
        raise RuntimeError("SoX not found. Install via Homebrew:  brew install sox")
    else:
        raise RuntimeError("SoX not found. Install via:  sudo apt-get install sox")
