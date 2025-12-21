import pandas as pd
from typing import Any, Dict
from .config import AppConfig
from .preprocessing import translate
from .audit import AuditLogger
from .feedback import FeedbackLog
from .models import CategorizeModel, FraudDetectionModel, GoalTrackingModel
from .intelligence import spending_exceeds_income_alert
from .performance import Timer

class FinanceAIEngine:
    def __init__(self, cfg: AppConfig):
        self.cfg = cfg
        self.audit = AuditLogger()
        self.feedback = FeedbackLog()
        self.data = None

        # Instantiate specialized models
        self.categorizer = CategorizeModel(cfg, self.audit, self.feedback)
        self.fraud_detector = FraudDetectionModel(cfg, self.audit, self.feedback)
        self.goal_tracker = GoalTrackingModel(cfg, self.audit, self.feedback)

    def load_data(self, path: str) -> pd.DataFrame:
        with Timer('Data Loading'):
            df = pd.read_csv(path)
            self.data = translate(df, self.cfg)
        return self.data

    def run_monthly_alerts(self) -> int:
        if self.data is None:
            return 0
        with Timer('Monthly Alerts'):
            return spending_exceeds_income_alert(self.data, self.audit, self.cfg)

    def goal_feasibility(self, user_id: int, target_amount: float, months_to_deadline: int):
        """Unified goal feasibility check using GoalTrackingModel."""
        return self.goal_tracker.predict_feasibility(user_id, self.data, target_amount, months_to_deadline)

    def category_retrain_ready(self):
        return self.feedback.prepare_category_training(self.cfg.category_retrain_min_feedback)

    # Unified Modeling Engine: train any model with Early Stopping via the base class
    def train_model(self, model_class, x_train, y_train, input_shape: int = None, output_shape: int = None,
                   batch_size: int = 32, epochs: int = 50, validation_split: float = 0.2,
                   patience: int = 8, acc_gap_margin: float = 0.05, plot_path: str = None) -> Dict:
        """
        Generic training interface for any model (CategorizeModel, FraudDetectionModel, GoalTrackingModel).
        """
        model = model_class(self.cfg, self.audit, self.feedback)
        if hasattr(model, 'build_network') and input_shape is not None:
            model.build_network(input_shape)
        elif input_shape is not None:
            model.compile_model(input_shape, output_shape or 1)

        result = model.train_with_early_stopping(
            x_train, y_train,
            batch_size=batch_size, epochs=epochs,
            validation_split=validation_split, patience=patience,
            acc_gap_margin=acc_gap_margin
        )

        if result.get('ok'):
            plot_file = model.plot_loss_history(plot_path)
            result['plot_file'] = plot_file

        return result

    def quick_predict_category(self, features) -> Dict[str, Any]:
        """Fast-track category prediction (< 50ms)."""
        with Timer('Quick Category'):
            return self.categorizer.predict_category(features)

    def quick_predict_fraud(self, features, txn_id=None, user_id=None) -> Dict[str, Any]:
        """Fast-track fraud detection (< 50ms)."""
        with Timer('Quick Fraud'):
            return self.fraud_detector.predict_fraud(features, txn_id, user_id)

    def quick_goal_check(self, user_id: int, target: float, months: int) -> Dict[str, Any]:
        """Fast-track goal feasibility (< 100ms)."""
        with Timer('Quick Goal'):
            return self.goal_tracker.predict_feasibility(user_id, self.data, target, months)
