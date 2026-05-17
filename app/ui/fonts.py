from __future__ import annotations

import ctypes
import sys
from pathlib import Path

FR_PRIVATE = 0x10


def _resource(relative: str) -> Path:
    base = Path(sys._MEIPASS) if hasattr(sys, "_MEIPASS") else Path(__file__).parent.parent.parent
    return base / relative


def load_bundled_fonts() -> None:
    """Register bundled fonts for this process only."""
    font_path = _resource("assets/fonts/Oswald-VF.ttf")
    if not font_path.exists():
        return
    ctypes.windll.gdi32.AddFontResourceExW(str(font_path), FR_PRIVATE, 0)
