import math
import tkinter as tk
from tkinter import Canvas

# Arc geometry: 0° = 7 o'clock (min), 300° = 5 o'clock (max), clockwise
_START_CANVAS_ANGLE = -120.0
_ARC_SPAN  = 300.0
_MIN_VAL   = 15
_MAX_VAL   = 120
_STEP      = 5

ACCENT          = "#CAFF3C"
_TRACK_LIGHT    = "#C8C4BD"
_TRACK_DARK     = "#3A3A3A"
_HANDLE_LIGHT   = "#111111"
_HANDLE_DARK    = "#FFFFFF"
_BG_LIGHT       = "#F0EDE6"
_BG_DARK        = "#111111"
_TEXT_LIGHT     = "#111111"
_TEXT_DARK      = "#F6F4EF"
_MUTED_LIGHT    = "#888480"
_MUTED_DARK     = "#666666"


def value_to_dial_angle(value: int) -> float:
    fraction = (value - _MIN_VAL) / (_MAX_VAL - _MIN_VAL)
    return fraction * _ARC_SPAN


def dial_angle_to_value(dial_angle: float) -> int:
    fraction = max(0.0, min(1.0, dial_angle / _ARC_SPAN))
    raw      = _MIN_VAL + fraction * (_MAX_VAL - _MIN_VAL)
    snapped  = round(raw / _STEP) * _STEP
    return max(_MIN_VAL, min(_MAX_VAL, snapped))


def mouse_to_dial_angle(mx: float, my: float, cx: float, cy: float) -> float:
    dx  = mx - cx
    dy  = cy - my
    ang = math.degrees(math.atan2(dy, dx))
    result = (_START_CANVAS_ANGLE - ang) % 360
    return result if result != 360.0 else 0.0


def dial_angle_to_canvas_angle(dial_angle: float) -> float:
    return _START_CANVAS_ANGLE - dial_angle


class DialWidget(tk.Frame):
    """Circular timer dial. Range 15–120 min, step 5 min."""

    def __init__(
        self,
        master,
        size: int = 220,
        on_change=None,
        dark: bool = False,
        display_font: str = "Impact",
        label_font: str = "Oswald",
        **kwargs,
    ) -> None:
        bg = _BG_DARK if dark else _BG_LIGHT
        super().__init__(master, bg=bg, **kwargs)
        self._size         = size
        self._on_change    = on_change
        self._dark         = dark
        self._display_font = display_font
        self._label_font   = label_font
        self._value        = 45
        self._center_text_id: int = 0

        self._canvas = Canvas(
            self, width=size, height=size,
            bg=bg, highlightthickness=0,
        )
        self._canvas.pack()
        self._canvas.bind("<ButtonPress-1>", self._on_press)
        self._canvas.bind("<B1-Motion>",     self._on_drag)
        self._canvas.bind("<ButtonRelease-1>", self._on_release)
        self._draw()

    def set_value(self, value: int) -> None:
        self._value = max(_MIN_VAL, min(_MAX_VAL, value))
        self._draw()

    def get_value(self) -> int:
        return self._value

    def set_center_text(self, text: str) -> None:
        if self._center_text_id:
            self._canvas.itemconfig(self._center_text_id, text=text)

    def set_dark(self, dark: bool) -> None:
        self._dark = dark
        bg = _BG_DARK if dark else _BG_LIGHT
        self._canvas.config(bg=bg)
        self.config(bg=bg)
        self._draw()

    # ── Drawing ────────────────────────────────────────────────────────────

    def _draw(self) -> None:
        c = self._canvas
        c.delete("all")
        s  = self._size
        cx = cy = s / 2

        margin = s * 0.09
        r_arc  = (s - 2 * margin) / 2

        track  = _TRACK_DARK  if self._dark else _TRACK_LIGHT
        handle = _HANDLE_DARK if self._dark else _HANDLE_LIGHT
        text   = _TEXT_DARK   if self._dark else _TEXT_LIGHT
        muted  = _MUTED_DARK  if self._dark else _MUTED_LIGHT

        # ── Tick marks ─────────────────────────────────────────────────────
        n_ticks = 25
        for i in range(n_ticks):
            da    = i * (_ARC_SPAN / (n_ticks - 1))
            ca    = math.radians(dial_angle_to_canvas_angle(da))
            major = i % 4 == 0
            r_out = r_arc + 1
            r_in  = r_arc * (0.80 if major else 0.88)
            c.create_line(
                cx + r_out * math.cos(ca), cy - r_out * math.sin(ca),
                cx + r_in  * math.cos(ca), cy - r_in  * math.sin(ca),
                fill=track, width=(2 if major else 1),
            )

        # ── Background track arc ───────────────────────────────────────────
        c.create_arc(
            margin, margin, s - margin, s - margin,
            start=_START_CANVAS_ANGLE, extent=-_ARC_SPAN,
            style="arc", outline=track, width=2,
        )

        # ── Filled accent arc ──────────────────────────────────────────────
        dial_angle = value_to_dial_angle(self._value)
        if dial_angle > 0:
            c.create_arc(
                margin, margin, s - margin, s - margin,
                start=_START_CANVAS_ANGLE, extent=-dial_angle,
                style="arc", outline=ACCENT, width=10,
            )

        # ── Handle dot ─────────────────────────────────────────────────────
        ca    = math.radians(dial_angle_to_canvas_angle(dial_angle))
        hx    = cx + r_arc * math.cos(ca)
        hy    = cy - r_arc * math.sin(ca)
        dot_r = s * 0.058
        c.create_oval(
            hx - dot_r, hy - dot_r, hx + dot_r, hy + dot_r,
            fill=handle, outline="",
        )

        # ── Center value ───────────────────────────────────────────────────
        num_fs = int(s * 0.30)   # large number
        self._center_text_id = c.create_text(
            cx, cy - num_fs * 0.14,
            text=str(self._value),
            font=(self._display_font, num_fs, "bold"),
            fill=text,
        )
        # "МИНУТ" sublabel
        sub_fs = int(s * 0.09)
        c.create_text(
            cx, cy + num_fs * 0.70,
            text="МИНУТ",
            font=(self._label_font, sub_fs, "bold"),
            fill=muted,
        )

    # ── Mouse interaction ──────────────────────────────────────────────────

    def _on_press(self, event) -> None:
        self._update_from_mouse(event.x, event.y)

    def _on_drag(self, event) -> None:
        self._update_from_mouse(event.x, event.y)

    def _on_release(self, _event) -> None:
        pass

    def _update_from_mouse(self, mx: float, my: float) -> None:
        cx = cy = self._size / 2
        dial_angle = mouse_to_dial_angle(mx, my, cx, cy)
        if dial_angle > _ARC_SPAN:
            dial_angle = _ARC_SPAN if dial_angle < _ARC_SPAN + 30 else 0.0
        new_val = dial_angle_to_value(dial_angle)
        if new_val != self._value:
            self._value = new_val
            self._draw()
            if self._on_change:
                self._on_change(new_val)
