import io
import json
import os
import runpy
import unittest
from unittest.mock import patch
from urllib.parse import parse_qs


class EchoTest(unittest.TestCase):
    def test_echoes_text_and_media_and_retries_only_failed_send(self):
        updates = [
            {"update_id": 41, "message": {"chat": {"id": 7}, "text": "Привет + &"}},
            {"update_id": 42, "message": {"chat": {"id": 7}, "photo": []}},
            {"update_id": 43, "message": {"chat": {"id": 8}, "sticker": {"file_id": "sticker-id"}}},
            {"update_id": 44, "message": {"chat": {"id": 9}, "voice": {"file_id": "voice-id"}}},
            {
                "update_id": 45,
                "message": {"chat": {"id": 10}, "video_note": {"file_id": "note-id"}},
            },
        ]
        offsets = []
        sent = []

        def telegram(request, *, timeout):
            self.assertEqual(timeout, 40)
            self.assertEqual(request.get_method(), "POST")
            method = request.full_url.rsplit("/", 1)[-1]
            params = parse_qs(request.data.decode(), strict_parsing=True)
            if method == "getUpdates":
                self.assertEqual(params["allowed_updates"], ['["message"]'])
                offset = int(params["offset"][0])
                offsets.append(offset)
                if len(offsets) == 3:
                    raise KeyboardInterrupt
                result = [update for update in updates if update["update_id"] >= offset]
                payload = {"ok": True, "result": result}
            else:
                sent.append((method, params))
                if method == "sendVideoNote" and len(sent) == 4:
                    payload = {"ok": False, "description": "Временная ошибка"}
                else:
                    payload = {"ok": True, "result": {"message_id": 99}}
            return io.BytesIO(json.dumps(payload).encode())

        with (
            patch.dict(
                os.environ,
                {"BASE_URL": "https://telegram.invalid", "TELEGRAM_TOKEN": "test"},
            ),
            patch("urllib.request.urlopen", side_effect=telegram),
            patch("time.sleep") as sleep,
            self.assertLogs("bot", level="INFO"),
        ):
            runpy.run_module("bot", run_name="__main__")

        self.assertEqual(
            sent,
            [
                ("sendMessage", {"chat_id": ["7"], "text": ["Привет + &"]}),
                ("sendSticker", {"chat_id": ["8"], "sticker": ["sticker-id"]}),
                ("sendVoice", {"chat_id": ["9"], "voice": ["voice-id"]}),
                ("sendVideoNote", {"chat_id": ["10"], "video_note": ["note-id"]}),
                ("sendVideoNote", {"chat_id": ["10"], "video_note": ["note-id"]}),
            ],
        )
        self.assertEqual(offsets, [0, 45, 46])
        sleep.assert_called_once_with(5)
