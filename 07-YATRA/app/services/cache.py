import time

_cache:dict[str, dict] = {}

def get_cache(key: str) -> dict | None:
    if key in _cache:
        entry = _cache[key]
        if time.time() < entry["expiry"]:
            return entry["data"]
        else:
            del _cache[key]  # Remove expired entry

def set_cache(key: str, data: dict, ttl: int = 300) -> None:
    _cache[key] = {
        "data": data,
        "expiry": time.time() + ttl
    }

def clear_cache() -> None:
    _cache.clear()  