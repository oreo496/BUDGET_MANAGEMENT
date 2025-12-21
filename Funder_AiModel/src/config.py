from dataclasses import dataclass
from typing import Optional, List

@dataclass
class AppConfig:
    project_name: str = "FinanceAI"
    min_months_history: int = 2
    category_retrain_min_feedback: int = 10
    timezone: str = "UTC"
    
    train_dataset_path: Optional[str] = "final_train_dataset.csv"
    test_dataset_path: Optional[str] = "final_test_dataset.csv"
    
    numeric_amount_columns: List[str] = ("amount", "transaction_amount", "value", "amt")
    possible_date_columns: List[str] = ("transaction_date", "date", "timestamp", "created_at")
