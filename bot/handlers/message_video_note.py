from bot.handlers.handler import Handler, HandlerStatus
from bot.messenger import Messenger, Update


class MessageVideoNoteHandler(Handler):
    def can_handle(self, update: Update) -> bool:
        message = update.get("message")
        return isinstance(message, dict) and "video_note" in message

    def handle(self, update: Update, messenger: Messenger) -> HandlerStatus:
        message = update["message"]
        messenger.send_video_note(
            chat_id=message["chat"]["id"],
            video_note=message["video_note"]["file_id"],
        )
        return HandlerStatus.STOP
