from abc import ABC, abstractmethod
from enum import Enum, auto

from bot.messenger import Messenger, Update


class HandlerStatus(Enum):
    CONTINUE = auto()
    STOP = auto()


class Handler(ABC):
    @abstractmethod
    def can_handle(self, update: Update) -> bool:
        raise NotImplementedError

    @abstractmethod
    def handle(self, update: Update, messenger: Messenger) -> HandlerStatus:
        raise NotImplementedError
