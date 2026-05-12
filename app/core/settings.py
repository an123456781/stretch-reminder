import json
import os
from pathlib import Path
from types import MappingProxyType

DEFAULTS = MappingProxyType({
    "interval_minutes": 45,
    "theme": "system",
})


def _settings_path() -> Path:
    appdata = os.environ.get("APPDATA", str(Path.home()))
    return Path(appdata) / "StretchReminder" / "settings.json"


def load() -> dict:
    path = _settings_path()
    if not path.exists():
        save(DEFAULTS.copy())
        return DEFAULTS.copy()
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        return {**DEFAULTS, **data}
    except (json.JSONDecodeError, OSError):
        return DEFAULTS.copy()


def save(data: dict) -> None:
    path = _settings_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
