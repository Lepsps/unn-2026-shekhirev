from bot.handlers.handler import Handler, HandlerStatus
from bot.messenger import Messenger, Update


class MessageStickerHandler(Handler):
    def can_handle(self, update: Update) -> bool:
        message = update.get("message")
        return isinstance(message, dict) and "sticker" in message

    def handle(self, update: Update, messenger: Messenger) -> HandlerStatus:
        message = update["message"]
        messenger.send_sticker(
            chat_id=message["chat"]["id"],
            sticker=message["sticker"]["file_id"],
        )
        return HandlerStatus.STOP
