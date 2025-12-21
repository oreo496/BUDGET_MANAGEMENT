from typing import Callable, Any

class DataQualityGuard:
    def __init__(self, min_rows: int = 10):
        self.min_rows = min_rows
    def ensure(self, df) -> bool:
        try:
            return df is not None and len(df) >= self.min_rows
        except Exception:
            return False

def safe_call(fn: Callable[..., Any], *args, **kwargs):
    try:
        return {'ok': True, 'value': fn(*args, **kwargs), 'error': None}
    except Exception as e:
        return {'ok': False, 'value': None, 'error': str(e)}
