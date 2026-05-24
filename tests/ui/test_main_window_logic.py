from app.ui.main_window import MainWindow


def test_timer_finish_notifies_and_stops_without_restart():
    window = object.__new__(MainWindow)
    calls = []

    window._running = True
    window._notifier_fn = lambda: calls.append("notify")
    window._stop_timer = lambda: calls.append("stop")
    window._restart_timer = lambda: calls.append("restart")

    MainWindow._on_timer_finish(window)

    assert calls == ["notify", "stop"]


def test_timer_finish_does_nothing_when_already_stopped():
    window = object.__new__(MainWindow)
    calls = []

    window._running = False
    window._notifier_fn = lambda: calls.append("notify")
    window._stop_timer = lambda: calls.append("stop")

    MainWindow._on_timer_finish(window)

    assert calls == []
