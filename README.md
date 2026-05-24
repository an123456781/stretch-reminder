# Stretch Reminder

Небольшое Windows-приложение, которое напоминает встать и размяться через выбранный интервал времени.

## Возможности

- интервалы от 15 до 120 минут;
- круговой dial и быстрые пресеты;
- системные Windows-уведомления со звуком;
- работа из трея;
- светлая и тёмная тема;
- автоматическое сохранение выбранного интервала и темы.

## Скачать и попробовать

Самый простой способ — скачать готовый файл **`StretchReminder.exe`** из раздела **Releases** на GitHub и запустить его.

Установка не требуется. После запуска приложение появится в окне и в системном трее Windows.

## Как пользоваться

1. Выбери интервал напоминания — кнопками или перетаскиванием ручки на dial.
2. Нажми **СТАРТ**.
3. При желании закрой окно крестиком: приложение останется работать в трее.
4. Когда таймер сработает, Windows покажет уведомление, проиграет звук и остановит отсчёт.
5. Нажми **СТАРТ** снова, чтобы запустить новое напоминание.

## Настройки

Приложение автоматически сохраняет:

- выбранный интервал;
- светлую или тёмную тему.

Файл настроек хранится в:

```text
%APPDATA%\StretchReminder\settings.json
```

## Запуск из исходников

### Требования

- Windows 10/11;
- Python 3.12+.

### Установка

```bash
git clone https://github.com/an123456781/stretch-reminder.git
cd stretch-reminder
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## Сборка `.exe`

```bash
python scripts/make_icon.py
pyinstaller build.spec
```

Готовый файл появится здесь:

```text
dist/StretchReminder.exe
```

Подробности см. в [`docs/BUILDING.md`](docs/BUILDING.md).

## Структура проекта

```text
app/
  core/       логика таймера и настроек
  services/   уведомления и трей
  ui/         окно, dial и шрифты
assets/       иконка и встроенные шрифты
scripts/      вспомогательные скрипты
```

## Используемые технологии

- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) — интерфейс;
- [pystray](https://github.com/moses-palmer/pystray) — системный трей;
- [winotify](https://github.com/versa-syahptr/winotify) — Windows-уведомления;
- [PyInstaller](https://pyinstaller.org) — сборка standalone `.exe`;
- [Oswald](https://github.com/google/fonts/tree/main/ofl/oswald) — встроенный display-шрифт, лицензия SIL Open Font License.

## Лицензия

Код проекта распространяется по лицензии [MIT](LICENSE).

Встроенный шрифт Oswald распространяется отдельно по лицензии SIL Open Font License; текст лицензии лежит в [`assets/fonts/OFL.txt`](assets/fonts/OFL.txt).
