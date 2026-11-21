from bot.handlers.handler import Handler, HandlerStatus
from bot.messenger import Messenger, Update


class MessageVoiceHandler(Handler):
    def can_handle(self, update: Update) -> bool:
        message = update.get("message")
        return isinstance(message, dict) and "voice" in message

    def handle(self, update: Update, messenger: Messenger) -> HandlerStatus:
        message = update["message"]
        messenger.send_voice(
            chat_id=message["chat"]["id"],
            voice=message["voice"]["file_id"],
        )
        return HandlerStatus.STOP
