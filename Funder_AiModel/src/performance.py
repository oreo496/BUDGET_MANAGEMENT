from functools import lru_cache, wraps
from typing import Optional, Callable, Any
import time
import hashlib
import pickle

class FastCache:
    """
    High-speed LRU cache for predictions, validation, and expensive operations.
    Uses function signature + data hash for cache keys.
    """
    def __init__(self, max_size: int = 1024, ttl_seconds: int = 3600):
        self.max_size = max_size
        self.ttl = ttl_seconds
        self.cache = {}
        self.timestamps = {}

    def _key(self, func_name: str, *args, **kwargs) -> str:
        try:
            # Hash arguments to create cache key
            key_data = f"{func_name}_{str(args)}_{str(sorted(kwargs.items()))}"
            return hashlib.md5(key_data.encode()).hexdigest()
        except Exception:
            return None

    def get(self, key: str) -> Optional[Any]:
        if key is None:
            return None
        if key not in self.cache:
            return None
        # Check TTL
        if time.time() - self.timestamps.get(key, 0) > self.ttl:
            del self.cache[key]
            del self.timestamps[key]
            return None
        return self.cache[key]

    def set(self, key: str, value: Any) -> None:
        if key is None:
            return
        if len(self.cache) >= self.max_size:
            # Evict oldest entry
            oldest = min(self.timestamps, key=self.timestamps.get)
            del self.cache[oldest]
            del self.timestamps[oldest]
        self.cache[key] = value
        self.timestamps[key] = time.time()

    def clear(self):
        self.cache.clear()
        self.timestamps.clear()

    def cached(self, func: Callable) -> Callable:
        """Decorator to cache function results."""
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = self._key(func.__name__, *args, **kwargs)
            cached_val = self.get(key)
            if cached_val is not None:
                return cached_val
            result = func(*args, **kwargs)
            self.set(key, result)
            return result
        return wrapper


# Global cache instance
_global_cache = FastCache(max_size=2048, ttl_seconds=3600)


class Timer:
    """Utility to measure inference latency."""
    def __init__(self, name: str = "Operation"):
        self.name = name
        self.start_time = None

    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, *args):
        elapsed = (time.time() - self.start_time) * 1000
        print(f"[TIME] {self.name}: {elapsed:.1f}ms", flush=True)

    def elapsed_ms(self) -> float:
        if self.start_time is None:
            return 0.0
        return (time.time() - self.start_time) * 1000


class PerformanceConfig:
    """Configuration for real-time optimization."""
    BATCH_SIZE_PREDICT = 32  # Batch multiple predictions together
    CACHE_PREDICTIONS = True  # Cache model outputs
    VERBOSE_TRAINING = 0  # Silence training logs
    VERBOSE_INFERENCE = 0  # Silence prediction logs
    TF_DEVICE = '/CPU:0'  # Use CPU for faster inference on small batches
    NUM_THREADS = 4  # For parallel data loading
