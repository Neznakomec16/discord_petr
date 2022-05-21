import json
from pathlib import Path
from typing import List

from core.kill_counter.kill_counter_interface import KillCounterInterface
from core.kill_counter.constants import COUNT_EMOJI


class FileKillCounter(KillCounterInterface):
    def __init__(self, file_path: Path):
        self._kill_file_path = file_path
        if not file_path.exists():
            with open(file_path, "w") as f:
                f.write("{}")

    def get_kill_count(self, user_id: str):
        with open(self._kill_file_path, "r") as f:
            data = json.load(f)
        return data.get(user_id) or 0

    def increment_kill_count(self, user_id: str) -> int:
        with open(self._kill_file_path, "r") as f:
            data = json.load(f)
        if data.get(user_id) is None:
            data[user_id] = 0
        data[user_id] += 1
        with open(self._kill_file_path, "w") as f:
            json.dump(data, f)
        return data[user_id]

    def get_emoji_kill_count(self, user_id) -> List[str]:
        count = self.get_kill_count(user_id)
        result = []
        while count > 0:
            result.append(COUNT_EMOJI[count % 10])
            count = count // 10
        return result[::-1]
