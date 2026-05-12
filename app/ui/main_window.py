from __future__ import annotations

import sys
import time
from pathlib import Path
from typing import Callable

import customtkinter as ctk

from app.ui.dial_widget import DialWidget
from app.core.timer import Timer
from app.core import settings

ACCENT = "#CAFF3C"
_ACCENT_FG = "#111111"
_BG = ("#F0EDE6", "#111111")   # (light, dark) CTk color tuple
_FG = ("#111111", "#FFFFFF")
_BORDER = ("#111111", "#FFFFFF")
_PRESETS = [15, 30, 45, 60, 90, 120]
_W, _H = 380, 630


def _resource(relative: str) -> Path:
    base = Path(sys._MEIPASS) if hasattr(sys, "_MEIPASS") else Path(__file__).parent.parent.parent
    return base / relative


class MainWindow(ctk.CTk):
    def __init__(self, timer: Timer, notifier_fn: Callable, on_quit: Callable) -> None:
        super().__init__()
        self._timer = timer
        self._notifier_fn = notifier_fn
        self._on_quit = on_quit
        self._status_cb: Callable[[bool], None] | None = None

        cfg = settings.load()
        self._interval: int = cfg.get("interval_minutes", 45)
        self._running = False
        self._start_time = 0.0

        ctk.set_appearance_mode(cfg.get("theme", "system"))

        self.title("Stretch Reminder")
        self.geometry(f"{_W}x{_H}")
        self.resizable(False, False)
        self.configure(fg_color=_BG)
        self.protocol("WM_DELETE_WINDOW", self.hide)

        icon = _resource("assets/icon.ico")
        if icon.exists():
            self.iconbitmap(str(icon))

        self._build_ui()
        self._highlight_preset(self._interval)

    # ── public ───────────────────────────────────────────────────────────

    def hide(self) -> None:
        self.withdraw()

    def show(self) -> None:
        self.deiconify()
        self.lift()

    def set_status_callback(self, cb: Callable[[bool], None]) -> None:
        self._status_cb = cb

    # ── layout ────────────────────────────────────────────────────────────

    def _build_ui(self) -> None:
        # theme toggle
        tf = ctk.CTkFrame(self, fg_color="transparent")
        tf.pack(anchor="ne", padx=14, pady=(10, 0))
        for symbol, mode in [("☀", "Light"), ("🌙", "Dark")]:
            ctk.CTkButton(
                tf, text=symbol, width=34, height=26,
                font=ctk.CTkFont(size=13),
                fg_color=_BG, text_color=_FG,
                hover_color=ACCENT, border_width=1, border_color=_BORDER,
                corner_radius=6,
                command=lambda m=mode: self._set_theme(m),
            ).pack(side="left", padx=2)

        # title
        ctk.CTkLabel(
            self, text="ПОРА\nРАЗМЯТЬСЯ",
            font=ctk.CTkFont(family="Arial Black", size=46, weight="bold"),
            text_color=_FG, justify="left",
        ).pack(anchor="w", padx=20, pady=(0, 2))

        ctk.CTkLabel(
            self, text="НАПОМИНАТЬ ЧЕРЕЗ",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=_FG,
        ).pack()

        # dial row
        row = ctk.CTkFrame(self, fg_color="transparent")
        row.pack(pady=(4, 0))
        ctk.CTkLabel(row, text="15\nМИН", font=ctk.CTkFont(size=11),
                     text_color=_FG, justify="center").pack(side="left", padx=(0, 4))

        dark = ctk.get_appearance_mode() == "Dark"
        self._dial = DialWidget(row, size=210, on_change=self._on_dial_change, dark=dark)
        self._dial.pack(side="left")
        self._dial.set_value(self._interval)

        ctk.CTkLabel(row, text="120\nМИН", font=ctk.CTkFont(size=11),
                     text_color=_FG, justify="center").pack(side="left", padx=(4, 0))

        # preset buttons (2×3 grid)
        pf = ctk.CTkFrame(self, fg_color="transparent")
        pf.pack(pady=(8, 0), padx=20)
        self._preset_btns: dict[int, ctk.CTkButton] = {}
        for i, val in enumerate(_PRESETS):
            btn = ctk.CTkButton(
                pf, text=f"{val} МИН", width=100, height=32,
                font=ctk.CTkFont(size=12, weight="bold"),
                fg_color=_BG, text_color=_FG,
                border_width=1, border_color=_BORDER,
                corner_radius=4, hover_color=ACCENT,
                command=lambda v=val: self._select_preset(v),
            )
            btn.grid(row=i // 3, column=i % 3, padx=4, pady=3)
            self._preset_btns[val] = btn

        # start/stop
        self._start_btn = ctk.CTkButton(
            self, text="СТАРТ  →",
            font=ctk.CTkFont(family="Arial Black", size=22, weight="bold"),
            height=58, fg_color=ACCENT, text_color=_ACCENT_FG,
            hover_color="#B8E832", corner_radius=6,
            command=self._toggle_timer,
        )
        self._start_btn.pack(fill="x", padx=20, pady=(12, 0))

        ctk.CTkLabel(
            self, text="🪑  Стул не обидится, если ты встанешь.",
            font=ctk.CTkFont(size=11), text_color=_FG,
        ).pack(pady=(10, 0))

    # ── theme ─────────────────────────────────────────────────────────────

    def _set_theme(self, mode: str) -> None:
        ctk.set_appearance_mode(mode)
        self._dial.set_dark(mode == "Dark")
        cfg = settings.load()
        cfg["theme"] = mode
        settings.save(cfg)

    # ── interval selection ────────────────────────────────────────────────

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
        for val, btn in self._preset_btns.items():
            if val == active:
                btn.configure(fg_color=ACCENT, text_color=_ACCENT_FG, border_color=ACCENT)
            else:
                btn.configure(fg_color=_BG, text_color=_FG, border_color=_BORDER)

    # ── timer ──────────────────────────────────────────────────────────────

    def _toggle_timer(self) -> None:
        if self._running:
            self._stop_timer()
        else:
            self._start_timer()

    def _start_timer(self) -> None:
        self._running = True
        self._start_time = time.monotonic()
        self._start_btn.configure(text="СТОП  ✕")
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
        self._start_btn.configure(text="СТАРТ  →")
        self._dial.set_value(self._interval)
        if self._status_cb:
            self._status_cb(False)

    def _restart_timer(self) -> None:
        # _tick loop is still running (self._running stays True), so resetting
        # _start_time is sufficient — the next tick picks up the new time.
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
