class KeyCache:
    def __init__(self):
        self._cache = set()

    def __contains__(self, key):
        return key in self._cache

    def exists(self, key: str) -> bool:
        if key in self._cache:
            return True
        return False

    def add(self, key: str):
        return self._cache.add(key)

    def remove(self, key: str):
        if key in self._cache:
            return self._cache.remove(key)
