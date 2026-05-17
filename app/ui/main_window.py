from __future__ import annotations

import sys
import time
import tkinter as tk
from pathlib import Path
from typing import Callable

import customtkinter as ctk

from app.core import settings
from app.core.timer import Timer
from app.ui.dial_widget import DialWidget
from app.ui.fonts import load_bundled_fonts

ACCENT = "#CAFF3C"
_DISPLAY_FONT = "Oswald"
_UI_FONT = "Arial"
_LIGHT_BG = "#F0EDE6"
_DARK_BG = "#111111"
_LIGHT_FG = "#111111"
_DARK_FG = "#F6F4EF"
_LIGHT_MUTED = "#7E7A74"
_DARK_MUTED = "#8A8A8A"
_LIGHT_BORDER = "#111111"
_DARK_BORDER = "#F6F4EF"
_PRESETS = [15, 30, 45, 60, 90, 120]
_W, _H = 430, 760


def _resource(relative: str) -> Path:
    base = Path(sys._MEIPASS) if hasattr(sys, "_MEIPASS") else Path(__file__).parent.parent.parent
    return base / relative


class _CanvasButton(tk.Canvas):
    def __init__(
        self,
        master,
        *,
        width: int,
        height: int,
        text: str,
        command: Callable[[], None],
        fill: str,
        text_color: str,
        border: str,
        font: tuple,
        radius: int = 4,
    ) -> None:
        super().__init__(
            master,
            width=width,
            height=height,
            bg=master.cget("bg"),
            highlightthickness=0,
            bd=0,
        )
        self._command = command
        self._text = text
        self._fill = fill
        self._text_color = text_color
        self._border = border
        self._font = font
        self._radius = radius
        self.bind("<Button-1>", lambda _event: self._command())
        self._draw()

    def configure_style(self, *, fill: str, text_color: str, border: str) -> None:
        self._fill = fill
        self._text_color = text_color
        self._border = border
        self._draw()

    def set_text(self, text: str) -> None:
        self._text = text
        self._draw()

    def _draw(self) -> None:
        self.delete("all")
        w = int(self["width"])
        h = int(self["height"])
        self.create_rectangle(
            1,
            1,
            w - 1,
            h - 1,
            fill=self._fill,
            outline=self._border,
            width=1,
        )
        self.create_text(
            w / 2,
            h / 2,
            text=self._text,
            fill=self._text_color,
            font=self._font,
        )


class _ThemeToggle(tk.Canvas):
    def __init__(self, master, on_change: Callable[[str], None], dark: bool) -> None:
        super().__init__(
            master,
            width=110,
            height=42,
            bg=master.cget("bg"),
            highlightthickness=0,
            bd=0,
        )
        self._on_change = on_change
        self._dark = dark
        self.bind("<Button-1>", self._handle_click)
        self._draw()

    def set_dark(self, dark: bool) -> None:
        self._dark = dark
        self._draw()

    def _palette(self) -> tuple[str, str]:
        return (_DARK_FG, _DARK_BG) if self._dark else (_LIGHT_FG, _LIGHT_BG)

    def _draw(self) -> None:
        self.delete("all")
        fg, bg = self._palette()
        self.configure(bg=bg)
        self.create_rectangle(1, 1, 109, 41, outline=fg, width=1)
        self.create_line(55, 1, 55, 41, fill=fg, width=1)

        if self._dark:
            self.create_rectangle(55, 1, 109, 41, fill=_DARK_FG, outline="")
            left_fill, right_fill = _DARK_FG, _DARK_BG
        else:
            self.create_rectangle(1, 1, 55, 41, fill=_LIGHT_FG, outline="")
            left_fill, right_fill = _LIGHT_BG, _LIGHT_FG

        self._draw_sun(28, 21, left_fill)
        self._draw_moon(82, 21, right_fill)

    def _draw_sun(self, x: int, y: int, color: str) -> None:
        self.create_oval(x - 6, y - 6, x + 6, y + 6, outline=color, width=2)
        for dx, dy in [(0, -13), (0, 13), (-13, 0), (13, 0), (-9, -9), (9, -9), (-9, 9), (9, 9)]:
            self.create_line(x + dx * 0.65, y + dy * 0.65, x + dx, y + dy, fill=color, width=2)

    def _draw_moon(self, x: int, y: int, color: str) -> None:
        self.create_oval(x - 10, y - 10, x + 10, y + 10, outline=color, width=2)
        bg = _DARK_FG if self._dark else _LIGHT_BG
        self.create_oval(x - 2, y - 12, x + 12, y + 8, fill=bg, outline=bg)

    def _handle_click(self, event) -> None:
        self._on_change("Light" if event.x < 55 else "Dark")


class _HintBox(tk.Canvas):
    def __init__(self, master, dark: bool) -> None:
        super().__init__(master, width=392, height=70, highlightthickness=0, bd=0)
        self._dark = dark
        self._draw()

    def set_dark(self, dark: bool) -> None:
        self._dark = dark
        self._draw()

    def _draw(self) -> None:
        self.delete("all")
        bg = _DARK_BG if self._dark else _LIGHT_BG
        fg = _DARK_FG if self._dark else _LIGHT_FG
        self.configure(bg=bg)
        self.create_rectangle(1, 1, 391, 69, outline=fg, width=1)
        self.create_line(64, 1, 64, 69, fill=fg, width=1)

        # Chair icon
        self.create_line(25, 50, 25, 32, fill=fg, width=3)
        self.create_line(25, 32, 41, 32, fill=fg, width=3)
        self.create_line(41, 32, 41, 50, fill=fg, width=3)
        self.create_line(23, 50, 21, 59, fill=fg, width=3)
        self.create_line(43, 50, 45, 59, fill=fg, width=3)

        self.create_text(
            82,
            25,
            anchor="w",
            text="СТУЛ НЕ ОБИДИТСЯ,",
            fill=fg,
            font=(_UI_FONT, 12, "bold"),
        )
        self.create_text(
            82,
            45,
            anchor="w",
            text="ЕСЛИ ТЫ ВСТАНЕШЬ.",
            fill=fg,
            font=(_UI_FONT, 12, "bold"),
        )


class MainWindow(ctk.CTk):
    def __init__(self, timer: Timer, notifier_fn: Callable, on_quit: Callable) -> None:
        super().__init__()
        load_bundled_fonts()
        self._timer = timer
        self._notifier_fn = notifier_fn
        self._on_quit = on_quit
        self._status_cb: Callable[[bool], None] | None = None

        cfg = settings.load()
        self._interval: int = cfg.get("interval_minutes", 45)
        self._running = False
        self._start_time = 0.0
        self._dark = cfg.get("theme", "system").lower() == "dark"

        ctk.set_appearance_mode("Dark" if self._dark else "Light")

        self.title("Stretch Reminder")
        self.geometry(f"{_W}x{_H}")
        self.resizable(False, False)
        self.configure(fg_color=self._bg)
        self.protocol("WM_DELETE_WINDOW", self.hide)

        icon = _resource("assets/icon.ico")
        if icon.exists():
            self.iconbitmap(str(icon))

        self._shell = tk.Frame(self, bg=self._bg)
        self._shell.pack(fill="both", expand=True)

        self._build_ui()
        self._highlight_preset(self._interval)

    @property
    def _bg(self) -> str:
        return _DARK_BG if self._dark else _LIGHT_BG

    @property
    def _fg(self) -> str:
        return _DARK_FG if self._dark else _LIGHT_FG

    @property
    def _muted(self) -> str:
        return _DARK_MUTED if self._dark else _LIGHT_MUTED

    @property
    def _border(self) -> str:
        return _DARK_BORDER if self._dark else _LIGHT_BORDER

    def hide(self) -> None:
        self.withdraw()

    def show(self) -> None:
        self.deiconify()
        self.lift()

    def set_status_callback(self, cb: Callable[[bool], None]) -> None:
        self._status_cb = cb

    def _build_ui(self) -> None:
        header = tk.Frame(self._shell, bg=self._bg)
        header.pack(fill="x", padx=20, pady=(18, 0))

        self._theme_toggle = _ThemeToggle(header, self._set_theme, self._dark)
        self._theme_toggle.pack(side="right", pady=(8, 0))

        self._title = tk.Label(
            header,
            text="ПОРА\nРАЗМЯТЬСЯ",
            bg=self._bg,
            fg=self._fg,
            justify="left",
            anchor="w",
            font=(_DISPLAY_FONT, 56, "bold"),
            padx=0,
            pady=0,
        )
        self._title.pack(side="left", anchor="w")

        self._caption = tk.Label(
            self._shell,
            text="НАПОМИНАТЬ ЧЕРЕЗ",
            bg=self._bg,
            fg=self._fg,
            font=(_UI_FONT, 11, "bold"),
        )
        self._caption.pack(anchor="w", padx=20, pady=(12, 0))

        dial_row = tk.Frame(self._shell, bg=self._bg)
        dial_row.pack(pady=(8, 0))

        self._left_min = self._make_side_label(dial_row, "15")
        self._left_min.pack(side="left", padx=(0, 12))

        self._dial = DialWidget(dial_row, size=250, on_change=self._on_dial_change, dark=self._dark)
        self._dial.pack(side="left")
        self._dial.set_value(self._interval)

        self._right_min = self._make_side_label(dial_row, "120")
        self._right_min.pack(side="left", padx=(12, 0))

        presets = tk.Frame(self._shell, bg=self._bg)
        presets.pack(pady=(12, 0))
        self._preset_btns: dict[int, _CanvasButton] = {}
        for i, value in enumerate(_PRESETS):
            btn = _CanvasButton(
                presets,
                width=124,
                height=42,
                text=f"{value} МИН",
                command=lambda v=value: self._select_preset(v),
                fill=self._bg,
                text_color=self._fg,
                border=self._border,
                font=(_UI_FONT, 12, "bold"),
            )
            btn.grid(row=i // 3, column=i % 3, padx=4, pady=4)
            self._preset_btns[value] = btn

        self._start_btn = _CanvasButton(
            self._shell,
            width=392,
            height=68,
            text="СТАРТ      →",
            command=self._toggle_timer,
            fill=ACCENT,
            text_color=_LIGHT_FG,
            border=ACCENT,
            font=(_DISPLAY_FONT, 30, "bold"),
        )
        self._start_btn.pack(pady=(16, 0))

        self._hint = _HintBox(self._shell, self._dark)
        self._hint.pack(pady=(12, 0))

    def _make_side_label(self, master, value: str) -> tk.Frame:
        frame = tk.Frame(master, bg=self._bg)
        tk.Label(
            frame,
            text=value,
            bg=self._bg,
            fg=self._fg,
            font=(_UI_FONT, 16, "bold"),
        ).pack()
        tk.Label(
            frame,
            text="МИН",
            bg=self._bg,
            fg=self._fg,
            font=(_UI_FONT, 11, "bold"),
        ).pack()
        return frame

    def _set_theme(self, mode: str) -> None:
        self._dark = mode == "Dark"
        ctk.set_appearance_mode(mode)
        self.configure(fg_color=self._bg)
        self._shell.configure(bg=self._bg)
        self._theme_toggle.set_dark(self._dark)
        self._title.configure(bg=self._bg, fg=self._fg)
        self._caption.configure(bg=self._bg, fg=self._fg)
        for frame in (self._left_min, self._right_min):
            frame.configure(bg=self._bg)
            for child in frame.winfo_children():
                child.configure(bg=self._bg, fg=self._fg)
        self._dial.set_dark(self._dark)
        self._hint.set_dark(self._dark)
        self._highlight_preset(self._interval)
        cfg = settings.load()
        cfg["theme"] = mode
        settings.save(cfg)

    def _select_preset(self, value: int) -> None:
        self._interval = value
        self._dial.set_value(value)
        self._highlight_preset(value)
        if self._running:
            self._restart_timer()
        cfg = settings.load()
        cfg["interval_minutes"] = value
        settings.save(cfg)

    def _on_dial_change(self, value: int) -> None:
        self._interval = value
        self._highlight_preset(value)
        if self._running:
            self._restart_timer()
        cfg = settings.load()
        cfg["interval_minutes"] = value
        settings.save(cfg)

    def _highlight_preset(self, active: int) -> None:
        for value, button in self._preset_btns.items():
            if value == active:
                button.configure_style(fill=ACCENT, text_color=_LIGHT_FG, border=ACCENT)
            else:
                button.configure_style(fill=self._bg, text_color=self._fg, border=self._border)

    def _toggle_timer(self) -> None:
        if self._running:
            self._stop_timer()
        else:
            self._start_timer()

    def _start_timer(self) -> None:
        self._running = True
        self._start_time = time.monotonic()
        self._start_btn.set_text("СТОП       ×")
        if self._status_cb:
            self._status_cb(True)
        self._timer.start(
            duration_seconds=self._interval * 60,
            on_finish=lambda: self.after_idle(self._on_timer_finish),
        )
        self._tick()

    def _stop_timer(self) -> None:
        self._running = False
        self._timer.stop()
        self._start_btn.set_text("СТАРТ      →")
        self._dial.set_value(self._interval)
        if self._status_cb:
            self._status_cb(False)

    def _restart_timer(self) -> None:
        self._start_time = time.monotonic()
        self._timer.start(
            duration_seconds=self._interval * 60,
            on_finish=lambda: self.after_idle(self._on_timer_finish),
        )

    def _on_timer_finish(self) -> None:
        if not self._running:
            return
        self._notifier_fn()
        self._restart_timer()

    def _tick(self) -> None:
        if not self._running:
            return
        elapsed = int(time.monotonic() - self._start_time)
        remaining = max(0, self._interval * 60 - elapsed)
        mins, secs = divmod(remaining, 60)
        self._dial.set_center_text(f"{mins:02d}:{secs:02d}")
        self.after(1000, self._tick)
