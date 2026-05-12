import json
import pytest
from pathlib import Path
from unittest.mock import patch

import app.core.settings as settings


def test_load_creates_defaults_when_no_file(tmp_path):
    with patch.object(settings, "_settings_path", return_value=tmp_path / "settings.json"):
        result = settings.load()
    assert result["interval_minutes"] == 45
    assert result["theme"] == "system"
    assert (tmp_path / "settings.json").exists()


def test_load_merges_partial_data_with_defaults(tmp_path):
    path = tmp_path / "settings.json"
    path.write_text('{"interval_minutes": 30}', encoding="utf-8")
    with patch.object(settings, "_settings_path", return_value=path):
        result = settings.load()
    assert result["interval_minutes"] == 30
    assert result["theme"] == "system"


def test_save_writes_file_and_creates_dirs(tmp_path):
    path = tmp_path / "sub" / "settings.json"
    with patch.object(settings, "_settings_path", return_value=path):
        settings.save({"interval_minutes": 60, "theme": "dark"})
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data == {"interval_minutes": 60, "theme": "dark"}


def test_load_returns_defaults_on_corrupt_file(tmp_path):
    path = tmp_path / "settings.json"
    path.write_text("not json", encoding="utf-8")
    with patch.object(settings, "_settings_path", return_value=path):
        result = settings.load()
    assert result == settings.DEFAULTS
