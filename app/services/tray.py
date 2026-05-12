from __future__ import annotations

import sys
import threading
from pathlib import Path
from typing import Callable

from PIL import Image, ImageDraw
import pystray


def _icon_path() -> Path:
    base = Path(sys._MEIPASS) if hasattr(sys, "_MEIPASS") else Path(__file__).parent.parent.parent
    return base / "assets" / "icon.ico"


def _load_icon() -> Image.Image:
    path = _icon_path()
    if path.exists():
        return Image.open(path).convert("RGBA")
    img = Image.new("RGBA", (64, 64), (20, 20, 20, 255))
    draw = ImageDraw.Draw(img)
    draw.ellipse([16, 16, 48, 48], fill=(202, 255, 60, 255))
    return img


class Tray:
    def __init__(self, on_show_hide: Callable, on_quit: Callable) -> None:
        self._on_show_hide = on_show_hide
        self._on_quit = on_quit
        self._running = False
        self._icon: pystray.Icon | None = None

    def run_detached(self) -> None:
        menu = pystray.Menu(
            pystray.MenuItem("Показать / Скрыть", self._handle_show_hide, default=True),
            pystray.MenuItem(self._status_title, None, enabled=False),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Выход", self._handle_quit),
        )
        self._icon = pystray.Icon(
            "StretchReminder", _load_icon(), "Stretch Reminder", menu
        )
        threading.Thread(target=self._icon.run, daemon=True).start()

    def set_status(self, running: bool) -> None:
        self._running = running
        if self._icon:
            self._icon.update_menu()

    def stop(self) -> None:
        if self._icon:
            self._icon.stop()

    def _status_title(self, item) -> str:
        return "● Работает" if self._running else "○ Остановлен"

    def _handle_show_hide(self, icon, item) -> None:
        self._on_show_hide()

    def _handle_quit(self, icon, item) -> None:
        self._on_quit()
