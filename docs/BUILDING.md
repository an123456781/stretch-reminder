# Сборка Stretch Reminder

## Требования

- Windows 10/11;
- Python 3.12+;
- установленные зависимости из `requirements.txt`.

## Подготовка окружения

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Локальный запуск

```bash
python main.py
```

## Автоматические тесты

```bash
python -m pytest -v
```

## Сборка исполняемого файла

```bash
python scripts/make_icon.py
pyinstaller build.spec
```

Результат:

```text
dist/StretchReminder.exe
```

## Что включается в сборку

- иконка приложения;
- файлы CustomTkinter;
- встроенный шрифт Oswald;
- все Python-модули проекта.

## Проверка готовой сборки

После сборки рекомендуется проверить:

1. запуск `.exe`;
2. появление иконки в трее;
3. запуск и остановку таймера;
4. показ уведомления;
5. переключение светлой и тёмной темы;
6. повторный запуск приложения и восстановление настроек.
