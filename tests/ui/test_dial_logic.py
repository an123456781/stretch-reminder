import math
import pytest
from app.ui.dial_widget import (
    value_to_dial_angle,
    dial_angle_to_value,
    mouse_to_dial_angle,
    dial_angle_to_canvas_angle,
)


def test_minimum_value_maps_to_zero_angle():
    assert value_to_dial_angle(15) == pytest.approx(0.0)


def test_maximum_value_maps_to_300_angle():
    assert value_to_dial_angle(120) == pytest.approx(300.0)


def test_45_minutes_maps_to_correct_angle():
    # fraction = (45-15)/105 ≈ 0.2857, angle = 0.2857 * 300 ≈ 85.71
    assert value_to_dial_angle(45) == pytest.approx(85.71, abs=0.1)


def test_dial_angle_to_value_minimum():
    assert dial_angle_to_value(0.0) == 15


def test_dial_angle_to_value_maximum():
    assert dial_angle_to_value(300.0) == 120


def test_dial_angle_to_value_snaps_to_5_minutes():
    # dial_angle=50 → raw = 15 + 50/300*105 ≈ 32.5 → snapped to 30
    assert dial_angle_to_value(50.0) == 30


def test_dial_angle_to_value_clamps_below_min():
    assert dial_angle_to_value(-10.0) == 15


def test_dial_angle_to_value_clamps_above_max():
    assert dial_angle_to_value(310.0) == 120


def test_mouse_at_7_oclock_gives_zero_angle():
    # 7 o'clock in standard coords: atan2 angle = -120°
    cx, cy, r = 100.0, 100.0, 80.0
    rad = math.radians(-120)
    mx = cx + r * math.cos(rad)
    my = cy - r * math.sin(rad)  # screen coords (y down)
    assert mouse_to_dial_angle(mx, my, cx, cy) == pytest.approx(0.0, abs=0.1)


def test_mouse_at_5_oclock_gives_300_angle():
    # 5 o'clock in standard coords: atan2 angle = -60°
    cx, cy, r = 100.0, 100.0, 80.0
    rad = math.radians(-60)
    mx = cx + r * math.cos(rad)
    my = cy - r * math.sin(rad)
    assert mouse_to_dial_angle(mx, my, cx, cy) == pytest.approx(300.0, abs=0.1)


def test_canvas_angle_for_minimum_is_minus_120():
    assert dial_angle_to_canvas_angle(0.0) == pytest.approx(-120.0)


def test_canvas_angle_for_maximum_is_minus_420():
    # -120 - 300 = -420 (same screen position as -60, tkinter handles wrapping)
    assert dial_angle_to_canvas_angle(300.0) == pytest.approx(-420.0)
