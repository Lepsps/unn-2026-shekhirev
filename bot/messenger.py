from abc import ABC, abstractmethod
from typing import Any

Update = dict[str, Any]


class Messenger(ABC):
    @abstractmethod
    def get_updates(
        self,
        *,
        offset: int,
        limit: int,
        timeout: int,
        allowed_updates: list[str],
    ) -> list[Update]:
        raise NotImplementedError

    @abstractmethod
    def send_message(self, *, chat_id: int, text: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def send_sticker(self, *, chat_id: int, sticker: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def send_voice(self, *, chat_id: int, voice: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def send_video_note(self, *, chat_id: int, video_note: str) -> None:
        raise NotImplementedError
