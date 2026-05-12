import threading
from typing import Callable


class Timer:
    def __init__(self) -> None:
        self._thread: threading.Thread | None = None
        self._stop_event = threading.Event()

    def start(self, duration_seconds: int, on_finish: Callable) -> None:
        self.stop()
        self._stop_event.clear()
        self._thread = threading.Thread(
            target=self._run,
            args=(duration_seconds, on_finish),
            daemon=True,
        )
        self._thread.start()

    def stop(self) -> None:
        self._stop_event.set()
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=1)
        self._thread = None

    def is_running(self) -> bool:
        return self._thread is not None and self._thread.is_alive()

    def _run(self, duration_seconds: int, on_finish: Callable) -> None:
        cancelled = self._stop_event.wait(timeout=duration_seconds)
        if not cancelled:
            on_finish()
