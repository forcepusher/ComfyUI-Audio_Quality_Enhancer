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


if __name__ == "__main__":
    install_requirements()
