from bot.handlers.handler import Handler
from bot.handlers.message_sticker import MessageStickerHandler
from bot.handlers.message_text import MessageTextHandler
from bot.handlers.message_video_note import MessageVideoNoteHandler
from bot.handlers.message_voice import MessageVoiceHandler


def get_handlers() -> list[Handler]:
    return [
        MessageTextHandler(),
        MessageStickerHandler(),
        MessageVoiceHandler(),
        MessageVideoNoteHandler(),
    ]
