import pandas as pd
from typing import Dict
from .config import AppConfig

def validate_user_data(data_clean: pd.DataFrame, user_id, cfg: AppConfig) -> Dict:
    user_transactions = data_clean[data_clean['user_id'] == user_id] if 'user_id' in data_clean.columns else pd.DataFrame()
    if len(user_transactions) == 0:
        return {
            'status': 'ERR_INVALID_USER', 'user_id': user_id,
            'months_available': 0, 'transaction_count': 0,
            'is_valid': False, 'reason': 'User not found in transaction history'
        }
    date_col = None
    for col in cfg.possible_date_columns:
        if col in user_transactions.columns:
            date_col = col; break
    months_available = 1
    if date_col:
        try:
            dt = pd.to_datetime(user_transactions[date_col])
            months_available = max(1, int((dt.max() - dt.min()).days / 30))
        except Exception:
            months_available = 1
    else:
        months_available = max(1, len(user_transactions) // 10)
    txn_count = len(user_transactions)
    if months_available >= cfg.min_months_history and txn_count >= cfg.min_months_history * 5:
        status, is_valid = 'OK', True
    elif months_available >= 1 and txn_count >= 5:
        status, is_valid = 'ERR_MARGINAL_DATA', False
    else:
        status, is_valid = 'ERR_INSUFFICIENT_DATA', False
    return {
        'status': status, 'user_id': user_id, 'months_available': months_available,
        'transaction_count': txn_count, 'is_valid': is_valid,
        'min_months_required': cfg.min_months_history,
        'reason': 'Data validation passed' if is_valid else f'Only {months_available} month(s) available, {cfg.min_months_history} required'
    }
