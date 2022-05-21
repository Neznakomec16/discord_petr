from abc import ABC, abstractmethod
from typing import List


class KillCounterInterface(ABC):
    @abstractmethod
    def get_kill_count(self, user_id: str) -> int:
        ...

    @abstractmethod
    def increment_kill_count(self, user_id: str) -> int:
        ...

    @abstractmethod
    def get_emoji_kill_count(self, user_id: str) -> List[str]:
        ...
