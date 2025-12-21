import pandas as pd
from datetime import datetime, timezone, timedelta
import numpy as np
from .audit import AuditLogger
from .config import AppConfig

def spending_exceeds_income_alert(data_clean: pd.DataFrame, audit: AuditLogger, cfg: AppConfig) -> int:
    """
    Current month alert: Compare total income vs total expenses.
    Triggers CRITICAL alert if spending > income.
    """
    now = datetime.now()
    start = datetime(now.year, now.month, 1)
    next_month = (start + timedelta(days=32)).replace(day=1)
    
    df = data_clean.copy()
    date_col = next((c for c in cfg.possible_date_columns if c in df.columns), None)
    if date_col:
        df['_date_parsed'] = pd.to_datetime(df[date_col], errors='coerce')
        df = df[(df['_date_parsed'] >= start) & (df['_date_parsed'] < next_month)]
    
    amt_col = next((c for c in cfg.numeric_amount_columns if c in df.columns), None)
    if amt_col is None:
        num = df.select_dtypes(include=[np.number]).columns
        amt_col = num[0] if len(num) else None
    
    if amt_col is None or len(df) == 0:
        return 0
    
    alert_count = 0
    users = df['user_id'].unique().tolist() if 'user_id' in df.columns else [None]
    for uid in users:
        sub = df if uid is None else df[df['user_id'] == uid]
        amounts = sub[amt_col].dropna()
        total_income = float(amounts[amounts > 0].sum())
        total_expenses = float(abs(amounts[amounts < 0].sum()))
        
        if total_expenses > total_income and (total_income + total_expenses) > 0:
            audit.log(
                uid, 'budget_risk', 'HIGH',
                f"Total spending has exceeded total income for this month | income=${total_income:.2f}, expenses=${total_expenses:.2f}",
                None, None, None, None, 'SUFFICIENT_DATA', 'spending_vs_income_alert'
            )
            alert_count += 1
    
    return alert_count
