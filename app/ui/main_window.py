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

ACCENT        = "#CAFF3C"
_LIGHT_BG     = "#F0EDE6"
_DARK_BG      = "#111111"
_LIGHT_FG     = "#111111"
_DARK_FG      = "#F6F4EF"
_LIGHT_BORDER = "#111111"
_DARK_BORDER  = "#F6F4EF"
_PRESETS      = [15, 30, 45, 60, 90, 120]
_W, _H        = 430, 790


def _resource(relative: str) -> Path:
    base = Path(sys._MEIPASS) if hasattr(sys, "_MEIPASS") else Path(__file__).parent.parent.parent
    return base / relative


# ── Canvas-based rounded/sharp button ────────────────────────────────────────

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
        arrow: bool = False,
    ) -> None:
        super().__init__(
            master, width=width, height=height,
            bg=master.cget("bg"), highlightthickness=0, bd=0,
        )
        self._command    = command
        self._text       = text
        self._fill       = fill
        self._text_color = text_color
        self._border     = border
        self._font       = font
        self._arrow      = arrow
        self.bind("<Button-1>", lambda _e: self._command())
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self._hover = False
        self._draw()

    def configure_style(self, *, fill: str, text_color: str, border: str) -> None:
        self._fill = fill
        self._text_color = text_color
        self._border = border
        self._draw()

    def set_text(self, text: str) -> None:
        self._text = text
        self._draw()

    def _on_enter(self, _e) -> None:
        self._hover = True
        self._draw()

    def _on_leave(self, _e) -> None:
        self._hover = False
        self._draw()

    def _draw(self) -> None:
        self.delete("all")
        w = int(self["width"])
        h = int(self["height"])
        fill = self._fill
        if self._hover and fill == ACCENT:
            fill = "#D8FF50"
        # Inset by 1 so the 2px border is fully visible
        self.create_rectangle(1, 1, w - 1, h - 1, fill=fill, outline=self._border, width=2)
        if self._arrow:
            # Single centered text: "СТАРТ   →"
            self.create_text(
                w / 2, h / 2,
                text=f"{self._text}   →",
                fill=self._text_color,
                font=self._font,
                anchor="center",
            )
        else:
            self.create_text(
                w / 2, h / 2,
                text=self._text,
                fill=self._text_color,
                font=self._font,
            )


# ── Theme toggle: [☀ | ☽] ─────────────────────────────────────────────────

class _ThemeToggle(tk.Canvas):
    _W, _H = 84, 36

    def __init__(self, master, on_change: Callable[[str], None], dark: bool) -> None:
        super().__init__(
            master, width=self._W, height=self._H,
            bg=master.cget("bg"), highlightthickness=0, bd=0,
        )
        self._on_change = on_change
        self._dark = dark
        self.bind("<Button-1>", self._handle_click)
        self._draw()

    def set_dark(self, dark: bool) -> None:
        self._dark = dark
        self._draw()

    def _draw(self) -> None:
        self.delete("all")
        fg = _DARK_FG if self._dark else _LIGHT_FG
        bg = _DARK_BG if self._dark else _LIGHT_BG
        self.configure(bg=bg)
        W, H = self._W, self._H
        half = W // 2

        # Outer border
        self.create_rectangle(1, 1, W - 1, H - 1, outline=fg, width=2)
        # Divider
        self.create_line(half, 1, half, H - 1, fill=fg, width=2)

        if self._dark:
            self.create_rectangle(half, 1, W - 1, H - 1, fill=fg, outline="")
            sun_col  = fg
            moon_col = bg
        else:
            self.create_rectangle(1, 1, half, H - 1, fill=fg, outline="")
            sun_col  = bg
            moon_col = fg

        self._draw_sun(half // 2, H // 2, sun_col)
        self._draw_moon(half + half // 2, H // 2, moon_col, bg)

    def _draw_sun(self, x: int, y: int, color: str) -> None:
        r = 5
        self.create_oval(x - r, y - r, x + r, y + r, outline=color, width=2)
        for dx, dy in [(0, -11), (0, 11), (-11, 0), (11, 0),
                       (-8, -8), (8, -8), (-8, 8), (8, 8)]:
            self.create_line(
                x + dx * 0.6, y + dy * 0.6,
                x + dx * 0.95, y + dy * 0.95,
                fill=color, width=1,
            )

    def _draw_moon(self, x: int, y: int, color: str, bg: str) -> None:
        self.create_oval(x - 8, y - 8, x + 8, y + 8, outline=color, width=2)
        self.create_oval(x - 1, y - 9, x + 9, y + 6, fill=bg, outline=bg)

    def _handle_click(self, event) -> None:
        self._on_change("Light" if event.x < self._W // 2 else "Dark")


# ── Hint box: [chair icon | text] ─────────────────────────────────────────

class _HintBox(tk.Canvas):
    _W, _H = 390, 62

    def __init__(self, master, dark: bool, label_font: tuple) -> None:
        super().__init__(master, width=self._W, height=self._H,
                         highlightthickness=0, bd=0)
        self._dark = dark
        self._label_font = label_font
        self._draw()

    def set_dark(self, dark: bool) -> None:
        self._dark = dark
        self._draw()

    def _draw(self) -> None:
        self.delete("all")
        bg = _DARK_BG if self._dark else _LIGHT_BG
        fg = _DARK_FG if self._dark else _LIGHT_FG
        W, H = self._W, self._H
        self.configure(bg=bg)
        self.create_rectangle(1, 1, W - 1, H - 1, outline=fg, width=2)

        # Divider line
        icon_x = 56
        self.create_line(icon_x, 1, icon_x, H - 1, fill=fg, width=2)

        # ── Chair icon ────────────────────────────────
        cx = icon_x // 2
        cy = H // 2

        # Chair back (vertical rect top-left)
        self.create_rectangle(cx - 11, cy - 13, cx - 5, cy + 2,
                              fill=fg, outline="")
        # Seat (horizontal rect)
        self.create_rectangle(cx - 11, cy + 2, cx + 7, cy + 7,
                              fill=fg, outline="")
        # Left leg
        self.create_line(cx - 9, cy + 7, cx - 10, cy + 16, fill=fg, width=3)
        # Right leg
        self.create_line(cx + 5, cy + 7, cx + 6, cy + 16, fill=fg, width=3)
        # Arm rest top
        self.create_rectangle(cx - 11, cy - 13, cx + 7, cy - 9,
                              fill=fg, outline="")
        # Seat support
        self.create_line(cx - 2, cy - 9, cx - 2, cy + 2, fill=fg, width=3)

        # Text
        self.create_text(
            icon_x + 10, H // 2 - 9,
            anchor="w",
            text="СТУЛ НЕ ОБИДИТСЯ,",
            fill=fg, font=self._label_font,
        )
        self.create_text(
            icon_x + 10, H // 2 + 9,
            anchor="w",
            text="ЕСЛИ ТЫ ВСТАНЕШЬ.",
            fill=fg, font=self._label_font,
        )


# ── Main window ────────────────────────────────────────────────────────────

class MainWindow(ctk.CTk):
    def __init__(self, timer: Timer, notifier_fn: Callable, on_quit: Callable) -> None:
        super().__init__()
        self._display_font = load_bundled_fonts()   # "Impact" or "Noto Sans Condensed"
        self._label_font   = "Oswald"
        self._ui_font      = "Arial"

        self._timer       = timer
        self._notifier_fn = notifier_fn
        self._on_quit     = on_quit
        self._status_cb: Callable[[bool], None] | None = None

        cfg = settings.load()
        self._interval: int = cfg.get("interval_minutes", 45)
        self._running   = False
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
        # CTk may override tk.Frame bg after init — force correct colours
        self.after(50, lambda: self._recolor_frames(self._shell))

    # ── Palette helpers ────────────────────────────────────────────────────

    @property
    def _bg(self) -> str:
        return _DARK_BG if self._dark else _LIGHT_BG

    @property
    def _fg(self) -> str:
        return _DARK_FG if self._dark else _LIGHT_FG

    @property
    def _border(self) -> str:
        return _DARK_BORDER if self._dark else _LIGHT_BORDER

    # ── Window visibility ──────────────────────────────────────────────────

    def hide(self) -> None:
        self.withdraw()

    def show(self) -> None:
        self.deiconify()
        self.lift()

    def set_status_callback(self, cb: Callable[[bool], None]) -> None:
        self._status_cb = cb

    # ── UI construction ────────────────────────────────────────────────────

    def _build_ui(self) -> None:
        # ── Heading canvas — draws "ПОРА / РАЗМЯТЬСЯ" directly ────────────
        heading_font = (self._display_font, 75, "bold")
        self._heading = tk.Canvas(
            self._shell, width=_W - 40, height=240,
            bg=self._bg, highlightthickness=0, bd=0,
        )
        self._heading.pack(anchor="w", padx=20, pady=(14, 0))
        self._heading_font = heading_font
        self._draw_heading()

        # ── Theme toggle — created after heading so it sits on top (z-order)
        self._theme_toggle = _ThemeToggle(self._shell, self._set_theme, self._dark)
        self._theme_toggle.place(x=_W - 20 - _ThemeToggle._W, y=14)

        # ── "НАПОМИНАТЬ ЧЕРЕЗ" caption ─────────────────────────────────────
        self._caption = tk.Label(
            self._shell,
            text="НАПОМИНАТЬ ЧЕРЕЗ",
            bg=self._bg, fg=self._fg,
            font=(self._label_font, 10, "bold"),
            anchor="w",
        )
        self._caption.pack(anchor="w", padx=20, pady=(6, 0))

        # ── Dial row: [15 МИН] — [dial] — [120 МИН] ───────────────────────
        dial_row = tk.Frame(self._shell, bg=self._bg)
        dial_row.pack(pady=(4, 0))

        self._left_label = self._make_side_label(dial_row, "15")
        self._left_label.pack(side="left", padx=(0, 2))

        self._dash_l = tk.Label(
            dial_row, text="—", bg=self._bg, fg=self._fg,
            font=(self._label_font, 14, "bold"),
        )
        self._dash_l.pack(side="left", padx=(0, 4))

        self._dial = DialWidget(
            dial_row, size=220,
            on_change=self._on_dial_change,
            dark=self._dark,
            display_font=self._display_font,
            label_font=self._label_font,
        )
        self._dial.pack(side="left")
        self._dial.set_value(self._interval)

        self._dash_r = tk.Label(
            dial_row, text="—", bg=self._bg, fg=self._fg,
            font=(self._label_font, 14, "bold"),
        )
        self._dash_r.pack(side="left", padx=(4, 0))

        self._right_label = self._make_side_label(dial_row, "120")
        self._right_label.pack(side="left", padx=(2, 0))

        # ── Preset grid: 3 × 2 ────────────────────────────────────────────
        presets = tk.Frame(self._shell, bg=self._bg)
        presets.pack(pady=(10, 0))
        self._preset_btns: dict[int, _CanvasButton] = {}
        for i, value in enumerate(_PRESETS):
            btn = _CanvasButton(
                presets,
                width=122, height=40,
                text=f"{value} МИН",
                command=lambda v=value: self._select_preset(v),
                fill=self._bg,
                text_color=self._fg,
                border=self._border,
                font=(self._label_font, 11, "bold"),
            )
            btn.grid(row=i // 3, column=i % 3, padx=3, pady=3)
            self._preset_btns[value] = btn

        # ── СТАРТ button ───────────────────────────────────────────────────
        self._start_btn = _CanvasButton(
            self._shell,
            width=390, height=64,
            text="СТАРТ",
            command=self._toggle_timer,
            fill=ACCENT,
            text_color=_LIGHT_FG,
            border=ACCENT,
            font=(self._display_font, 28, "bold"),
            arrow=True,
        )
        self._start_btn.pack(pady=(12, 0))

        # ── Hint box ───────────────────────────────────────────────────────
        self._hint = _HintBox(
            self._shell, self._dark,
            label_font=(self._label_font, 11, "bold"),
        )
        self._hint.pack(pady=(10, 0))


    def _draw_heading(self) -> None:
        c = self._heading
        c.delete("all")
        fg = _DARK_FG if self._dark else _LIGHT_FG
        bg = _DARK_BG if self._dark else _LIGHT_BG
        c.configure(bg=bg)
        c.create_text(0, 0,   text="ПОРА",      font=self._heading_font, fill=fg, anchor="nw")
        c.create_text(0, 120, text="РАЗМЯТЬСЯ", font=self._heading_font, fill=fg, anchor="nw")

    def _make_side_label(self, master, value: str) -> tk.Frame:
        frame = tk.Frame(master, bg=self._bg)
        tk.Label(
            frame, text=value,
            bg=self._bg, fg=self._fg,
            font=(self._label_font, 16, "bold"),
        ).pack()
        tk.Label(
            frame, text="МИН",
            bg=self._bg, fg=self._fg,
            font=(self._label_font, 10, "bold"),
        ).pack()
        return frame

    # ── Theme ──────────────────────────────────────────────────────────────

    def _set_theme(self, mode: str) -> None:
        self._dark = mode == "Dark"
        ctk.set_appearance_mode(mode)
        self.configure(fg_color=self._bg)
        self._recolor_frames(self._shell)
        self._draw_heading()
        self._theme_toggle.set_dark(self._dark)
        self._dial.set_dark(self._dark)
        self._hint.set_dark(self._dark)
        self._highlight_preset(self._interval)
        cfg = settings.load()
        cfg["theme"] = mode
        settings.save(cfg)

    def _recolor_frames(self, widget) -> None:
        skip = (_CanvasButton, _ThemeToggle, _HintBox, DialWidget)
        if isinstance(widget, skip):
            return
        if isinstance(widget, tk.Canvas):
            widget.configure(bg=self._bg)
            return
        if isinstance(widget, tk.Frame):
            widget.configure(bg=self._bg)
        elif isinstance(widget, tk.Label):
            widget.configure(bg=self._bg, fg=self._fg)
        for child in widget.winfo_children():
            self._recolor_frames(child)

    # ── Preset selection ───────────────────────────────────────────────────

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
        for value, btn in self._preset_btns.items():
            if value == active:
                btn.configure_style(fill=ACCENT, text_color=_LIGHT_FG, border=ACCENT)
            else:
                btn.configure_style(fill=self._bg, text_color=self._fg,
                                    border=self._border)

    # ── Timer control ──────────────────────────────────────────────────────

    def _toggle_timer(self) -> None:
        if self._running:
            self._stop_timer()
        else:
            self._start_timer()

    def _start_timer(self) -> None:
        self._running = True
        self._start_time = time.monotonic()
        self._start_btn.set_text("СТОП")
        self._start_btn._arrow = False
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
        self._start_btn._arrow = True
        self._start_btn.set_text("СТАРТ")
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
        self._stop_timer()

    def _tick(self) -> None:
        if not self._running:
            return
        elapsed   = int(time.monotonic() - self._start_time)
        remaining = max(0, self._interval * 60 - elapsed)
        mins, secs = divmod(remaining, 60)
        self._dial.set_center_text(f"{mins:02d}:{secs:02d}")
        self.after(1000, self._tick)
