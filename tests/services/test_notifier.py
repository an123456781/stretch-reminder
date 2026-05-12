import winsound
from unittest.mock import patch, MagicMock


def test_notify_shows_toast_with_correct_content():
    mock_toast = MagicMock()
    mock_cls = MagicMock(return_value=mock_toast)
    with patch("app.services.notifier.Notification", mock_cls), \
         patch("app.services.notifier._WINOTIFY_AVAILABLE", True), \
         patch("winsound.PlaySound"):
        from app.services import notifier
        notifier.notify()
    mock_cls.assert_called_once_with(
        app_id="StretchReminder",
        title="Внимание:",
        msg="Ты снова стал частью стула. Пора размяться.",
    )
    mock_toast.show.assert_called_once()


def test_notify_still_plays_sound_if_toast_raises():
    mock_toast = MagicMock()
    mock_toast.show.side_effect = Exception("toast failed")
    with patch("app.services.notifier.Notification", MagicMock(return_value=mock_toast)), \
         patch("app.services.notifier._WINOTIFY_AVAILABLE", True), \
         patch("winsound.PlaySound") as mock_sound:
        from app.services import notifier
        notifier.notify()
    mock_sound.assert_called_once()


def test_notify_plays_system_exclamation():
    with patch("app.services.notifier._WINOTIFY_AVAILABLE", False), \
         patch("winsound.PlaySound") as mock_sound:
        from app.services import notifier
        notifier.notify()
    mock_sound.assert_called_with(
        "SystemExclamation",
        winsound.SND_ALIAS | winsound.SND_ASYNC,
    )
