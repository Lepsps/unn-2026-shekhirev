import logging
import time
from collections.abc import Iterator

from bot.dispatcher import Dispatcher
from bot.messenger import Messenger

RETRY_DELAY = 5
logger = logging.getLogger(__name__)


def poll_once(dispatcher: Dispatcher, messenger: Messenger, offset: int) -> Iterator[int]:
    updates = messenger.get_updates(
        offset=offset,
        limit=10,
        timeout=30,
        allowed_updates=["message"],
    )
    for update in updates:
        dispatcher.dispatch(update)
        offset = max(offset, update["update_id"] + 1)
        yield offset


def start_long_polling(dispatcher: Dispatcher, messenger: Messenger) -> None:
    offset = 0
    while True:
        try:
            for next_offset in poll_once(dispatcher, messenger, offset):
                offset = next_offset
        except (OSError, RuntimeError) as error:
            logger.warning(
                "Ошибка опроса (%s), повтор через %s с",
                type(error).__name__,
                RETRY_DELAY,
            )
            time.sleep(RETRY_DELAY)
