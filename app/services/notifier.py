import winsound

try:
    from winotify import Notification
    _WINOTIFY_AVAILABLE = True
except ImportError:
    _WINOTIFY_AVAILABLE = False

_APP_ID = "StretchReminder"
_TITLE = "Внимание:"
_MESSAGE = "Ты снова стал частью стула. Пора размяться."


def notify() -> None:
    if _WINOTIFY_AVAILABLE:
        try:
            toast = Notification(app_id=_APP_ID, title=_TITLE, msg=_MESSAGE)
            toast.show()
        except Exception:
            pass
    winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS | winsound.SND_ASYNC)
