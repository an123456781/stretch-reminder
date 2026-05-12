"""Manual test — run: python tests/ui/test_window_manual.py"""
if __name__ == "__main__":
    from app.core.timer import Timer
    from app.ui.main_window import MainWindow

    win = MainWindow(
        timer=Timer(),
        notifier_fn=lambda: print("NOTIFY fired"),
        on_quit=lambda: win.destroy(),
    )
    win.mainloop()
