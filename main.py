import sys
from app.core.timer import Timer
from app.services.notifier import notify
from app.services.tray import Tray
from app.ui.main_window import MainWindow


def main() -> None:
    timer = Timer()
    window: MainWindow | None = None
    tray: Tray | None = None

    def toggle_window() -> None:
        if window and window.winfo_viewable():
            window.hide()
        elif window:
            window.show()

    def quit_app() -> None:
        timer.stop()
        if tray:
            tray.stop()
        if window:
            window.destroy()
        sys.exit(0)

    window = MainWindow(timer=timer, notifier_fn=notify, on_quit=quit_app)
    tray = Tray(on_show_hide=toggle_window, on_quit=quit_app)
    window.set_status_callback(tray.set_status)

    tray.run_detached()
    window.mainloop()


if __name__ == "__main__":
    main()
