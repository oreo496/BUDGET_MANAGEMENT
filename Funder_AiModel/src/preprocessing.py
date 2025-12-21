import pandas as pd
from typing import Tuple, List
from .config import AppConfig

def detect_columns(df: pd.DataFrame, cfg: AppConfig) -> Tuple[str, str]:
    date_col = next((c for c in cfg.possible_date_columns if c in df.columns), None)
    amount_col = next((c for c in cfg.numeric_amount_columns if c in df.columns), None)
    if amount_col is None:
        num = df.select_dtypes(include=['number']).columns
        amount_col = num[0] if len(num) else None
    return date_col, amount_col

def drop_redundant_columns(df: pd.DataFrame) -> Tuple[pd.DataFrame, List[str]]:
    """
    Drop non-predictive columns (IDs, metadata) that waste memory during model training.
    
    Removed columns:
    - ID columns: transaction_id, user_id, account_id (database indexing only)
    - Metadata: merchant_name, transaction_date, notes (human-readable, not predictive)
    
    Args:
        df: Input DataFrame
    
    Returns:
        Tuple of (cleaned DataFrame, list of dropped column names)
    """
    redundant_cols = [
        'transaction_id', 'user_id', 'account_id',  # Database IDs
        'merchant_name', 'transaction_date', 'notes'  # Metadata
    ]
    
    # Only drop columns that actually exist in the dataframe
    cols_to_drop = [c for c in redundant_cols if c in df.columns]
    
    if cols_to_drop:
        df_cleaned = df.drop(columns=cols_to_drop)
        return df_cleaned, cols_to_drop
    
    return df, []

def translate(df: pd.DataFrame, cfg: AppConfig) -> pd.DataFrame:
    # Normalize date and amount columns
    date_col, amount_col = detect_columns(df, cfg)
    out = df.copy()
    if date_col:
        out['_date_parsed'] = pd.to_datetime(out[date_col], errors='coerce')
    if amount_col:
        out['_amount'] = pd.to_numeric(out[amount_col], errors='coerce')
    # Lowercase transaction_type if present
    if 'transaction_type' in out.columns:
        out['transaction_type'] = out['transaction_type'].astype(str).str.lower()
    
    # Drop redundant columns to save memory
    out, _ = drop_redundant_columns(out)
    
    return out
