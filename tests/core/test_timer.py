import time
import pytest
from app.core.timer import Timer


def test_callback_fires_after_duration():
    fired = []
    timer = Timer()
    timer.start(duration_seconds=1, on_finish=lambda: fired.append(True))
    time.sleep(1.4)
    assert fired == [True]


def test_stop_prevents_callback():
    fired = []
    timer = Timer()
    timer.start(duration_seconds=2, on_finish=lambda: fired.append(True))
    time.sleep(0.1)
    timer.stop()
    time.sleep(2.2)
    assert fired == []


def test_is_running_reflects_state():
    timer = Timer()
    assert not timer.is_running()
    timer.start(duration_seconds=2, on_finish=lambda: None)
    assert timer.is_running()
    timer.stop()
    assert not timer.is_running()


def test_restart_replaces_existing_countdown():
    fired = []
    timer = Timer()
    timer.start(duration_seconds=5, on_finish=lambda: fired.append("first"))
    time.sleep(0.1)
    timer.start(duration_seconds=1, on_finish=lambda: fired.append("second"))
    time.sleep(1.4)
    assert fired == ["second"]
    timer.stop()
