"""
Installation script for ComfyUI-SlopAudio.
Called automatically by ComfyUI-Manager during installation.
"""

import subprocess
import sys
import os


def install_requirements():
    requirements_path = os.path.join(os.path.dirname(__file__), "requirements.txt")
    if os.path.exists(requirements_path):
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", requirements_path]
        )


def install_sox():
    sys.path.insert(0, os.path.dirname(__file__))
    from sox_utils import download_sox

    download_sox()


if __name__ == "__main__":
    install_requirements()
    install_sox()
