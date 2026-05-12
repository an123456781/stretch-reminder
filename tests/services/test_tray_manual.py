"""Manual test — run: python tests/services/test_tray_manual.py"""
import time
from app.services.tray import Tray

tray = Tray(
    on_show_hide=lambda: print("show/hide"),
    on_quit=lambda: (tray.stop(), exit()),
)
tray.run_detached()
print("Check system tray. Press Ctrl+C or click Выход to exit.")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    tray.stop()
