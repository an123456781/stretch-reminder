from __future__ import annotations

import ctypes
import sys
from pathlib import Path

FR_PRIVATE = 0x10

DISPLAY_FONT = "Bahnschrift SemiBold Condensed"   # heavy condensed system font — updated if NotoSans downloaded
LABEL_FONT = "Oswald"     # condensed, all weights registered below


def _resource(relative: str) -> Path:
    base = Path(sys._MEIPASS) if hasattr(sys, "_MEIPASS") else Path(__file__).parent.parent.parent
    return base / relative


def load_bundled_fonts() -> str:
    """Load bundled fonts. Returns the best available display font name."""
    global DISPLAY_FONT

    noto = _resource("assets/fonts/NotoSansCondensed-Black.ttf")
    if noto.exists():
        ok = ctypes.windll.gdi32.AddFontResourceExW(str(noto), FR_PRIVATE, 0)
        if ok:
            DISPLAY_FONT = "Noto Sans Condensed"

    oswald = _resource("assets/fonts/Oswald-VF.ttf")
    if oswald.exists():
        ctypes.windll.gdi32.AddFontResourceExW(str(oswald), FR_PRIVATE, 0)

    return DISPLAY_FONT
