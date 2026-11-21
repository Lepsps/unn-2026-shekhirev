import unittest
from unittest.mock import call, create_autospec

from bot.handlers.handler import HandlerStatus
from bot.handlers.message_sticker import MessageStickerHandler
from bot.handlers.message_text import MessageTextHandler
from bot.handlers.message_video_note import MessageVideoNoteHandler
from bot.handlers.message_voice import MessageVoiceHandler
from bot.messenger import Messenger


class MessageHandlerTest(unittest.TestCase):
    cases = (
        (MessageTextHandler, "text", "Привет!", call.send_message(chat_id=42, text="Привет!")),
        (
            MessageStickerHandler,
            "sticker",
            {"file_id": "s1"},
            call.send_sticker(chat_id=42, sticker="s1"),
        ),
        (MessageVoiceHandler, "voice", {"file_id": "v1"}, call.send_voice(chat_id=42, voice="v1")),
        (
            MessageVideoNoteHandler,
            "video_note",
            {"file_id": "n1"},
            call.send_video_note(chat_id=42, video_note="n1"),
        ),
    )

    def test_only_accepts_its_message_type(self):
        for handler_class, selected_type, _, _ in self.cases:
            handler = handler_class()
            with self.subTest(handler=handler_class.__name__, message_type=None):
                self.assertFalse(handler.can_handle({"update_id": 1}))
            for _, incoming_type, content, _ in self.cases:
                with self.subTest(handler=handler_class.__name__, message_type=incoming_type):
                    update = {
                        "update_id": 1,
                        "message": {"chat": {"id": 42}, incoming_type: content},
                    }
                    self.assertEqual(handler.can_handle(update), incoming_type == selected_type)

    def test_echoes_the_original_content_then_stops_the_chain(self):
        for handler_class, field, content, expected_call in self.cases:
            with self.subTest(handler=handler_class.__name__):
                messenger = create_autospec(Messenger, instance=True, spec_set=True)
                update = {"update_id": 1, "message": {"chat": {"id": 42}, field: content}}

                status = handler_class().handle(update, messenger)

                self.assertIs(status, HandlerStatus.STOP)
                self.assertEqual(messenger.mock_calls, [expected_call])
