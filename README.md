# Stretch Reminder

Напоминает, что тело — не мебель.

## Скачать

Скачай `StretchReminder.exe` из [Releases](../../releases) и запусти. Установка не нужна.

## Как пользоваться

1. Выбери интервал напоминания (15–120 мин) — ручкой на диале или кнопками
2. Нажми **СТАРТ**
3. Сверни в трей (крестик не закрывает приложение, а прячет его)
4. Получай напоминания каждые N минут, пока не нажмёшь **СТОП**

Настройки (интервал и тема) сохраняются автоматически.

## Разработка

**Требования:** Python 3.12+

```bash
pip install -r requirements.txt
python main.py
```

**Тесты:**
```bash
python -m pytest tests/core/ tests/services/ tests/ui/test_dial_logic.py -v
```

**Сборка .exe:**
```bash
python scripts/make_icon.py   # один раз при первой настройке
pyinstaller build.spec
# результат: dist/StretchReminder.exe
```

## Стек

- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) — UI
- [pystray](https://github.com/moses-palmer/pystray) — трей
- [winotify](https://github.com/versa-syahptr/winotify) — уведомления Windows
- [PyInstaller](https://pyinstaller.org) — сборка .exe
