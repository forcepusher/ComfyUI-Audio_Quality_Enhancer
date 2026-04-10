"""
SoX binary management for ComfyUI-SlopAudio.
Static SoX binaries are shipped in bin/{platform}/ for Windows, Linux, and macOS.
No downloads — everything is embedded.
"""

import os
import stat
import sys

_EXTENSION_DIR = os.path.dirname(os.path.abspath(__file__))
_BIN_DIR = os.path.join(_EXTENSION_DIR, "bin")

_PLATFORM_DIRS = {
    "win32": "win32",
    "darwin": "darwin",
    "linux": "linux",
}

_cached_sox_path: str | None = None


def _platform_key() -> str:
    if sys.platform == "win32":
        return "win32"
    if sys.platform == "darwin":
        return "darwin"
    return "linux"


def _get_embedded_sox() -> str | None:
    """Return path to the embedded SoX binary for the current platform, or None."""
    key = _platform_key()
    plat_dir = os.path.join(_BIN_DIR, _PLATFORM_DIRS[key])

    if key == "win32":
        candidate = os.path.join(plat_dir, "sox.exe")
    else:
        candidate = os.path.join(plat_dir, "sox")

    if not os.path.isfile(candidate):
        return None

    if key != "win32" and not os.access(candidate, os.X_OK):
        exe_bits = stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
        read_bits = stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH
        os.chmod(candidate, os.stat(candidate).st_mode | exe_bits | read_bits)

    if key == "linux":
        _setup_linux_ld_preload(plat_dir)

    return candidate


_LINUX_SHARED_LIBS = [
    "libbz2.so.1.0",
    "libgomp.so.1",
    "libgsm.so.1",
    "libltdl.so.7",
    "liblzma.so.5",
    "libm.so.6",
    "libmagic.so.1",
    "libpng16.so.16",
    "libpthread.so.0",
    "libsox.so.3",
    "libz.so.1",
]


def _setup_linux_ld_preload(plat_dir: str) -> None:
    """Set LD_PRELOAD so the bundled shared libraries are found at runtime."""
    prev = os.environ.get("LD_PRELOAD", "")
    paths = [prev] if prev else []
    for lib in _LINUX_SHARED_LIBS:
        lib_path = os.path.join(plat_dir, lib)
        if os.path.isfile(lib_path):
            paths.append(lib_path)
    if paths:
        os.environ["LD_PRELOAD"] = os.pathsep.join(paths)


def ensure_sox() -> str:
    """Return the path to the embedded SoX executable or raise."""
    global _cached_sox_path
    if _cached_sox_path and os.path.isfile(_cached_sox_path):
        return _cached_sox_path

    sox = _get_embedded_sox()
    if sox:
        _cached_sox_path = sox
        return sox

    key = _platform_key()
    expected = os.path.join(_BIN_DIR, _PLATFORM_DIRS[key])
    raise RuntimeError(
        f"Embedded SoX binary not found. Expected in: {expected}\n"
        "The bin/ directory should have been included with the extension. "
        "Re-install or re-clone the repository to restore it."
    )
