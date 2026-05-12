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
_TRACK_LIGHT = "#CCCCCC"
_TRACK_DARK = "#555555"
_HANDLE_LIGHT = "#111111"
_HANDLE_DARK = "#FFFFFF"
_BG_LIGHT = "#F0EDE6"
_BG_DARK = "#111111"


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
