import json
import urllib.parse
import urllib.request
from typing import Any

from bot.messenger import Messenger, Update

REQUEST_TIMEOUT = 40


class TelegramMessenger(Messenger):
    def __init__(self, token: str, base_url: str) -> None:
        self._url = f"{base_url.rstrip('/')}/bot{token}"

    def get_updates(
        self,
        *,
        offset: int,
        limit: int,
        timeout: int,
        allowed_updates: list[str],
    ) -> list[Update]:
        updates: list[Update] = self._request(
            "getUpdates",
            offset=offset,
            limit=limit,
            timeout=timeout,
            allowed_updates=json.dumps(allowed_updates),
        )
        return updates

    def send_message(self, *, chat_id: int, text: str) -> None:
        self._request("sendMessage", chat_id=chat_id, text=text)

    def send_sticker(self, *, chat_id: int, sticker: str) -> None:
        self._request("sendSticker", chat_id=chat_id, sticker=sticker)

    def send_voice(self, *, chat_id: int, voice: str) -> None:
        self._request("sendVoice", chat_id=chat_id, voice=voice)

    def send_video_note(self, *, chat_id: int, video_note: str) -> None:
        self._request("sendVideoNote", chat_id=chat_id, video_note=video_note)

    def _request(self, method: str, **params: object) -> Any:
        request = urllib.request.Request(
            f"{self._url}/{method}",
            data=urllib.parse.urlencode(params).encode(),
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=REQUEST_TIMEOUT) as response:
            payload = json.loads(response.read())
        if not payload["ok"]:
            raise RuntimeError(payload["description"])
        return payload["result"]
