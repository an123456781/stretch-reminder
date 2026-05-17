import math
import tkinter as tk
from tkinter import Canvas

# Arc geometry: 0° = 7 o'clock (min), 300° = 5 o'clock (max), clockwise
_START_CANVAS_ANGLE = -120.0   # 7 o'clock in tkinter canvas degrees (East=0, CCW positive)
_ARC_SPAN = 300.0              # total arc span in degrees
_MIN_VAL = 15
_MAX_VAL = 120
_STEP = 5

ACCENT = "#CAFF3C"
_DISPLAY_FONT = "Oswald"
_UI_FONT = "Arial"
_TRACK_LIGHT = "#111111"
_TRACK_DARK = "#666666"
_HANDLE_LIGHT = "#111111"
_HANDLE_DARK = "#FFFFFF"
_BG_LIGHT = "#F0EDE6"
_BG_DARK = "#111111"
_SUBLABEL_LIGHT = "#111111"
_SUBLABEL_DARK = "#F6F4EF"


def value_to_dial_angle(value: int) -> float:
    """Maps minutes [15..120] to dial angle [0..300] degrees (0=7 o'clock, clockwise)."""
    fraction = (value - _MIN_VAL) / (_MAX_VAL - _MIN_VAL)
    return fraction * _ARC_SPAN


def dial_angle_to_value(dial_angle: float) -> int:
    """Maps dial angle [0..300] to snapped minutes [15..120] in steps of 5."""
    fraction = max(0.0, min(1.0, dial_angle / _ARC_SPAN))
    raw = _MIN_VAL + fraction * (_MAX_VAL - _MIN_VAL)
    snapped = round(raw / _STEP) * _STEP
    return max(_MIN_VAL, min(_MAX_VAL, snapped))


def mouse_to_dial_angle(mx: float, my: float, cx: float, cy: float) -> float:
    """Converts mouse screen position to dial angle [0..360) where 0=7 o'clock, clockwise."""
    dx = mx - cx
    dy = cy - my  # flip y: screen coords (down=+) → math coords (up=+)
    atan_angle = math.degrees(math.atan2(dy, dx))
    result = (_START_CANVAS_ANGLE - atan_angle) % 360
    # Normalize 360 to 0
    return result if result != 360.0 else 0.0


def dial_angle_to_canvas_angle(dial_angle: float) -> float:
    """Converts dial angle to tkinter canvas angle (East=0, CCW positive)."""
    return _START_CANVAS_ANGLE - dial_angle


class DialWidget(tk.Frame):
    """Circular timer dial. Range 15–120 min, step 5 min."""

    def __init__(
        self,
        master,
        size: int = 220,
        on_change=None,
        dark: bool = False,
        **kwargs,
    ) -> None:
        bg = _BG_DARK if dark else _BG_LIGHT
        super().__init__(master, bg=bg, **kwargs)
        self._size = size
        self._on_change = on_change
        self._dark = dark
        self._value = 45
        self._center_text_id: int = 0

        self._canvas = Canvas(
            self, width=size, height=size,
            bg=bg, highlightthickness=0,
        )
        self._canvas.pack()
        self._canvas.bind("<ButtonPress-1>", self._on_press)
        self._canvas.bind("<B1-Motion>", self._on_drag)
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

    # ── drawing ──────────────────────────────────────────────────────────

    def _draw(self) -> None:
        c = self._canvas
        c.delete("all")
        s = self._size
        cx = cy = s / 2

        # Arc geometry — margin defines bounding box, r_arc is the actual radius
        margin = s * 0.08
        r_arc = (s - 2 * margin) / 2

        track = _TRACK_DARK if self._dark else _TRACK_LIGHT
        sublabel = _SUBLABEL_DARK if self._dark else _SUBLABEL_LIGHT
        handle_col = _HANDLE_DARK if self._dark else _HANDLE_LIGHT
        text_col = _HANDLE_DARK if self._dark else _HANDLE_LIGHT

        # Tick marks — sparse long markers like in the concept.
        n_ticks = 19
        for i in range(n_ticks):
            da = i * (_ARC_SPAN / (n_ticks - 1))
            ca = math.radians(dial_angle_to_canvas_angle(da))
            major = i % 3 == 0
            r_out = r_arc * 0.98
            r_in = r_arc * (0.82 if major else 0.89)
            c.create_line(
                cx + r_out * math.cos(ca), cy - r_out * math.sin(ca),
                cx + r_in  * math.cos(ca), cy - r_in  * math.sin(ca),
                fill=track, width=2 if major else 1,
            )

        # Background track arc
        c.create_arc(
            margin, margin, s - margin, s - margin,
            start=_START_CANVAS_ANGLE, extent=-_ARC_SPAN,
            style="arc", outline=track, width=1,
        )

        # Filled accent arc
        dial_angle = value_to_dial_angle(self._value)
        if dial_angle > 0:
            c.create_arc(
                margin, margin, s - margin, s - margin,
                start=_START_CANVAS_ANGLE, extent=-dial_angle,
                style="arc", outline=ACCENT, width=6,
            )

        # Handle dot — sits on the arc line
        ca = math.radians(dial_angle_to_canvas_angle(dial_angle))
        hx = cx + r_arc * math.cos(ca)
        hy = cy - r_arc * math.sin(ca)
        dot_r = s * 0.055
        c.create_oval(hx - dot_r, hy - dot_r, hx + dot_r, hy + dot_r,
                      fill=handle_col, outline="")

        # Center value — large Impact number
        fs = int(s * 0.25)
        self._center_text_id = c.create_text(
            cx, cy - fs * 0.18,
            text=str(self._value),
            font=(_DISPLAY_FONT, fs, "bold"),
            fill=text_col,
        )
        # "МИНУТ" sublabel
        sub_fs = int(s * 0.082)
        c.create_text(
            cx, cy + fs * 0.68,
            text="МИНУТ",
            font=(_UI_FONT, sub_fs, "bold"),
            fill=sublabel,
        )

    # ── mouse interaction ─────────────────────────────────────────────────

    def _on_press(self, event) -> None:
        self._update_from_mouse(event.x, event.y)

    def _on_drag(self, event) -> None:
        self._update_from_mouse(event.x, event.y)

    def _on_release(self, event) -> None:
        pass

    def _update_from_mouse(self, mx: float, my: float) -> None:
        cx = cy = self._size / 2
        dial_angle = mouse_to_dial_angle(mx, my, cx, cy)
        # Clamp angles outside arc to nearest endpoint
        if dial_angle > _ARC_SPAN:
            dial_angle = _ARC_SPAN if dial_angle < _ARC_SPAN + 30 else 0.0
        new_val = dial_angle_to_value(dial_angle)
        if new_val != self._value:
            self._value = new_val
            self._draw()
            if self._on_change:
                self._on_change(new_val)
