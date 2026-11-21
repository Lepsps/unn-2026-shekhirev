import logging
import os

from bot.dispatcher import Dispatcher
from bot.handlers import get_handlers
from bot.long_polling import start_long_polling
from bot.telegram_messenger import TelegramMessenger

logger = logging.getLogger("bot")


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    messenger = TelegramMessenger(
        token=os.environ["TELEGRAM_TOKEN"],
        base_url=os.environ["BASE_URL"],
    )
    dispatcher = Dispatcher(messenger)
    dispatcher.add_handlers(*get_handlers())
    try:
        start_long_polling(dispatcher, messenger)
    except KeyboardInterrupt:
        logger.info("Бот остановлен")


if __name__ == "__main__":
    main()
