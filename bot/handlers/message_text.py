from bot.handlers.handler import Handler, HandlerStatus
from bot.messenger import Messenger, Update


class MessageTextHandler(Handler):
    def can_handle(self, update: Update) -> bool:
        message = update.get("message")
        return isinstance(message, dict) and "text" in message

    def handle(self, update: Update, messenger: Messenger) -> HandlerStatus:
        message = update["message"]
        messenger.send_message(
            chat_id=message["chat"]["id"],
            text=message["text"],
        )
        return HandlerStatus.STOP
