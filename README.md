# Telegram-эхо-бот

Учебный бот повторяет текст, стикеры, голосовые сообщения и видеокружки в том же чате. Он получает сообщения через long polling и работает на стандартной библиотеке Python.

## Запуск

Нужен Python 3.14 или новее. Задайте `TELEGRAM_TOKEN` в окружении и выполните команду из корня репозитория.

```sh
TELEGRAM_BASE_URL=https://api.telegram.org python3 -m bot
```

Поддерживается и прежнее имя `BASE_URL`.

## Структура

- `bot/long_polling.py` получает обновления и сохраняет `offset` после обработки.
- `bot/dispatcher.py` выбирает обработчик из `bot/handlers/`.
- `bot/telegram_messenger.py` реализует интерфейс `Messenger` и отправляет запросы к Telegram Bot API.
- `tests/` содержит тесты на `unittest`, которые выполняются без подключения к Telegram.

## Проверки

`make test` запускает только тесты. Для полного набора проверок нужен `uv`.

```sh
make install
make check
```

`make check` проверяет форматирование, линтинг, типы и тесты. `make ruff-linter-fix ruff-cs-fix` применяет автоматические исправления Ruff.

GitHub Actions собирает Docker-образ и запускает проверки.

## Docker

```sh
make build
docker run --rm -e TELEGRAM_TOKEN -e TELEGRAM_BASE_URL=https://api.telegram.org echo-bot
```
