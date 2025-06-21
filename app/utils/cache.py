import threading
from typing import Any, Dict, Optional

class LocalCache:
    """
    Singleton para cache local de dados frequentes (ex: médicos, especializações).
    Thread-safe, com métodos para get/set/invalidate.
    """
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
                    cls._instance._cache = {}
        return cls._instance

    def get(self, key: str) -> Optional[Any]:
        return self._cache.get(key)

    def set(self, key: str, value: Any):
        self._cache[key] = value

    def invalidate(self, key: str):
        if key in self._cache:
            del self._cache[key]

    def clear(self):
        self._cache.clear()

# Instância global
cache = LocalCache()
