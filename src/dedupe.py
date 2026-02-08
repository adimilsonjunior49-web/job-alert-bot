import json
import os

class SeenStore:
    def __init__(self, path: str):
        self.path = path
        self._seen = set()
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    self._seen = set(json.load(f))
            except Exception:
                self._seen = set()

    def has(self, key: str) -> bool:
        return key in self._seen

    def add(self, key: str) -> None:
        self._seen.add(key)

    def save(self) -> None:
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(sorted(self._seen), f, ensure_ascii=False, indent=2)
