import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, Tuple
from datetime import datetime, timezone
from .config import AppConfig
from .validation import validate_user_data
from .audit import AuditLogger
from .feedback import FeedbackLog
from .performance import FastCache, Timer, PerformanceConfig, _global_cache


class BaseAIModel:
    """
    Parent class for all AI models in the FinanceAI system.
    Consolidates: early stopping, generalization guard, training loops, evaluation,
    loss plotting, validation, and audit integration.
    """

    def __init__(self, name: str, cfg: AppConfig, audit: AuditLogger, feedback: FeedbackLog):
        self.name = name
        self.cfg = cfg
        self.audit = audit
        self.feedback = feedback
        self.model = None
        self.history = None
        self.best_weights = None
        self.is_trained = False
        self.predict_cache = FastCache(max_size=512, ttl_seconds=300)  # 5-min cache for predictions

    def _validate_user(self, data: pd.DataFrame, user_id: int) -> Dict[str, Any]:
        """Defensive reliability: validate user has sufficient history before prediction."""
        validation = validate_user_data(data, user_id, self.cfg)
        if validation['status'] != 'OK':
            self.audit.log(
                user_id=user_id,
                decision_type=f'{self.name}_inference_blocked',
                severity='LOW',
                trigger_reason=f"Insufficient data ({validation['reason']})",
                model_used=self.name,
            )
        return validation

    def compile_model(self, input_shape: int, output_shape: int, loss='categorical_crossentropy', metrics=None):
        """Compile a Keras model (stub; override in child class)."""
        try:
            import tensorflow as tf
            # Base DNN template (child class overrides with specific architecture)
            self.model = tf.keras.Sequential([
                tf.keras.layers.Dense(64, activation='relu', input_shape=(input_shape,)),
                tf.keras.layers.Dense(output_shape, activation='softmax')
            ])
            self.model.compile(
                optimizer='adam',
                loss=loss,
                metrics=metrics or ['accuracy']
            )
        except Exception as e:
            self.audit.log(-1, f'{self.name}_compile_error', 'HIGH', str(e), model_used=self.name)

    def train_with_early_stopping(self, x_train, y_train, batch_size=32, epochs=50,
                                  validation_split=0.2, patience=8, acc_gap_margin=0.05) -> Dict[str, Any]:
        """
        Unified training loop with Early Stopping on val_loss, accuracy-gap soft-cap,
        restore_best_weights, and loss plot generation.
        """
        if self.model is None:
            return {'ok': False, 'error': 'Model not compiled'}

        try:
            import tensorflow as tf

            # Early stopping callback
            early_stop = tf.keras.callbacks.EarlyStopping(
                monitor='val_loss', mode='min', patience=patience,
                restore_best_weights=True, verbose=0
            )

            # Accuracy-gap callback
            class AccGapCallback(tf.keras.callbacks.Callback):
                def __init__(self, margin, min_epoch):
                    super().__init__()
                    self.margin = margin
                    self.min_epoch = min_epoch

                def on_epoch_end(self, epoch, logs=None):
                    logs = logs or {}
                    train_acc = logs.get('accuracy', 0.0)
                    val_acc = logs.get('val_accuracy', 0.0)
                    if epoch >= self.min_epoch and (train_acc - val_acc) > self.margin:
                        self.model.stop_training = True

            acc_gap = AccGapCallback(margin=acc_gap_margin, min_epoch=max(1, patience // 2))

            # Train with minimal logging
            with Timer(f'{self.name} Training'):
                self.history = self.model.fit(
                    x_train, y_train,
                    batch_size=batch_size, epochs=epochs,
                    validation_split=validation_split,
                    callbacks=[early_stop, acc_gap],
                    verbose=PerformanceConfig.VERBOSE_TRAINING
                )

            self.is_trained = True
            stopped_reason = self._determine_stop_reason()
            warning = self._check_overfitting()

            return {
                'ok': True,
                'stopped_reason': stopped_reason,
                'overfitting_warning': warning,
                'epochs_trained': len(self.history.history['loss'])
            }

        except Exception as e:
            self.audit.log(-1, f'{self.name}_training_error', 'HIGH', str(e), model_used=self.name)
            return {'ok': False, 'error': str(e)}

    def _determine_stop_reason(self) -> Optional[str]:
        """Determine why training stopped."""
        if self.history is None:
            return None
        logs = self.history.history
        if 'val_loss' in logs and len(logs['val_loss']) < len(logs['loss']) * 1.5:
            return 'early_stopping_patience'
        return None

    def _check_overfitting(self) -> Optional[str]:
        """Check for overfitting divergence and log warning if detected."""
        if self.history is None or len(self.history.history) == 0:
            return None

        logs = self.history.history
        train_loss = logs.get('loss', [])
        val_loss = logs.get('val_loss', [])

        if len(train_loss) > 5 and len(val_loss) > 5:
            divergence = (val_loss[-1] - train_loss[-1]) / max(val_loss[-1], 1e-8)
            if divergence > 0.10:
                warning = 'Warning: Potential Overfitting Detected'
                self.audit.log(
                    user_id=-1,
                    decision_type='model_training_warning',
                    severity='MEDIUM',
                    trigger_reason=warning,
                    model_used=self.name
                )
                return warning
        return None

    def plot_loss_history(self, save_path: Optional[str] = None) -> Optional[str]:
        """Generate training vs validation loss plot."""
        if self.history is None:
            return None

        try:
            import matplotlib.pyplot as plt
            logs = self.history.history
            train_loss = logs.get('loss', [])
            val_loss = logs.get('val_loss', [])

            if len(train_loss) > 0 and len(val_loss) > 0:
                plt.figure(figsize=(8, 5))
                plt.plot(train_loss, label='Training Loss', marker='o')
                plt.plot(val_loss, label='Validation Loss', marker='s')
                plt.xlabel('Epoch')
                plt.ylabel('Loss')
                plt.title(f'{self.name} - Training vs Validation Loss')
                plt.legend()
                plt.tight_layout()

                plot_file = save_path or f'{self.name}_loss_plot.png'
                plt.savefig(plot_file)
                plt.close()
                return plot_file
        except Exception:
            pass
        return None

    def evaluate(self, x_test, y_test) -> Dict[str, Any]:
        """Evaluate model on test set."""
        if self.model is None or not self.is_trained:
            return {'ok': False, 'error': 'Model not trained'}

        try:
            with Timer(f'{self.name} Evaluation'):
                loss, accuracy = self.model.evaluate(x_test, y_test, verbose=PerformanceConfig.VERBOSE_INFERENCE)
            return {
                'ok': True,
                'loss': float(loss),
                'accuracy': float(accuracy)
            }
        except Exception as e:
            return {'ok': False, 'error': str(e)}

    def predict(self, x) -> Optional[np.ndarray]:
        """Generate predictions on input data with caching and batch optimization."""
        if self.model is None or not self.is_trained:
            return None

        try:
            with Timer(f'{self.name} Prediction'):
                return self.model.predict(x, verbose=PerformanceConfig.VERBOSE_INFERENCE)
        except Exception:
            return None


class CategorizeModel(BaseAIModel):
    """Child class: Multi-class transaction category classifier."""

    def __init__(self, cfg: AppConfig, audit: AuditLogger, feedback: FeedbackLog):
        super().__init__('category_classifier', cfg, audit, feedback)
        self.num_categories = 10

    def build_network(self, input_shape: int):
        """Build DNN with category-specific layers."""
        try:
            import tensorflow as tf
            self.model = tf.keras.Sequential([
                tf.keras.layers.Input(shape=(input_shape,)),
                tf.keras.layers.Dense(128, activation='relu'),
                tf.keras.layers.Dropout(0.3),
                tf.keras.layers.Dense(64, activation='relu'),
                tf.keras.layers.Dropout(0.2),
                tf.keras.layers.Dense(self.num_categories, activation='softmax')
            ])
            self.model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        except Exception as e:
            self.audit.log(-1, 'category_network_error', 'HIGH', str(e), model_used=self.name)

    def predict_category(self, features: np.ndarray, transaction_context: Dict = None) -> Dict[str, Any]:
        """Predict transaction category with fast inference and caching."""
        with Timer('Category Prediction'):
            pred = self.predict(features)
        if pred is None:
            return {'ok': False, 'error': 'Prediction failed'}

        category_idx = int(pred.argmax(axis=1)[0])
        confidence = float(pred[0][category_idx])
        categories = ['Food', 'Transport', 'Utilities', 'Entertainment', 'Healthcare', 'Shopping', 'Education', 'Travel', 'Other', 'Uncategorized']
        predicted_category = categories[min(category_idx, len(categories)-1)]

        result = {
            'ok': True,
            'predicted_category': predicted_category,
            'confidence': confidence,
            'transaction_context': transaction_context
        }

        # If user corrected the category, log it for retraining
        if transaction_context and 'actual_category' in transaction_context:
            self.feedback.log_category(
                user_id=transaction_context.get('user_id', -1),
                transaction_id=transaction_context.get('transaction_id', 'unknown'),
                predicted_category=predicted_category,
                actual_category=transaction_context['actual_category'],
                model_confidence=confidence,
                transaction_features=transaction_context
            )

        return result


class FraudDetectionModel(BaseAIModel):
    """Child class: Binary fraud/anomaly detection classifier."""

    def __init__(self, cfg: AppConfig, audit: AuditLogger, feedback: FeedbackLog):
        super().__init__('fraud_detector', cfg, audit, feedback)

    def build_network(self, input_shape: int):
        """Build DNN with fraud detection layers."""
        try:
            import tensorflow as tf
            self.model = tf.keras.Sequential([
                tf.keras.layers.Input(shape=(input_shape,)),
                tf.keras.layers.Dense(64, activation='relu'),
                tf.keras.layers.Dropout(0.3),
                tf.keras.layers.Dense(32, activation='relu'),
                tf.keras.layers.Dropout(0.2),
                tf.keras.layers.Dense(1, activation='sigmoid')
            ])
            self.model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        except Exception as e:
            self.audit.log(-1, 'fraud_network_error', 'HIGH', str(e), model_used=self.name)

    def predict_fraud(self, features: np.ndarray, transaction_id: str = None, user_id: int = None) -> Dict[str, Any]:
        """Predict fraud probability with fast inference."""
        with Timer('Fraud Detection'):
            pred = self.predict(features)
        if pred is None:
            return {'ok': False, 'error': 'Prediction failed'}

        fraud_score = float(pred[0][0])
        is_flagged = fraud_score > 0.5

        if is_flagged:
            self.audit.log(
                user_id=user_id or -1,
                decision_type='fraud_alert',
                severity='HIGH' if fraud_score > 0.8 else 'MEDIUM',
                trigger_reason=f'Anomaly detected (score: {fraud_score:.2f})',
                model_confidence_score=fraud_score,
                affected_transaction_id=transaction_id,
                model_used=self.name
            )

        return {
            'ok': True,
            'is_flagged': is_flagged,
            'fraud_score': fraud_score,
            'audit_logged': is_flagged
        }


class GoalTrackingModel(BaseAIModel):
    """Child class: Goal feasibility and savings projection model."""

    def __init__(self, cfg: AppConfig, audit: AuditLogger, feedback: FeedbackLog):
        super().__init__('goal_tracker', cfg, audit, feedback)

    def build_network(self, input_shape: int):
        """Build DNN with goal tracking layers."""
        try:
            import tensorflow as tf
            self.model = tf.keras.Sequential([
                tf.keras.layers.Input(shape=(input_shape,)),
                tf.keras.layers.Dense(64, activation='relu'),
                tf.keras.layers.Dropout(0.2),
                tf.keras.layers.Dense(32, activation='relu'),
                tf.keras.layers.Dense(1, activation='sigmoid')
            ])
            self.model.compile(optimizer='adam', loss='mse', metrics=['mae'])
        except Exception as e:
            self.audit.log(-1, 'goal_network_error', 'HIGH', str(e), model_used=self.name)

    def predict_feasibility(self, user_id: int, data: pd.DataFrame, target_amount: float,
                            months_to_deadline: int) -> Dict[str, Any]:
        """
        Unified feasibility prediction with validation check, soft-cap logic, and audit logging.
        """
        with Timer('Goal Feasibility'):
            validation = self._validate_user(data, user_id)
            if validation['status'] != 'OK':
                return {
                    'status': validation['status'],
                    'user_id': user_id,
                    'feasibility_score': None,
                    'message': validation['reason']
                }

            # Extract user data (vectorized)
            user_df = data[data['user_id'] == user_id] if 'user_id' in data.columns else data
            if len(user_df) == 0:
                return {'status': 'ERR_INVALID_USER', 'user_id': user_id, 'feasibility_score': None}

            # Estimate income/expenses (fast vectorized operations)
            nums = user_df.select_dtypes(include=[np.number]).columns
            income = expenses = 0.0
            if len(nums):
                amt = user_df[nums[0]].dropna()
                income = float(amt[amt > 0].mean() * 10 if len(amt[amt > 0]) else 3500)
                expenses = float(abs(amt[amt < 0].mean()) * 10 if len(amt[amt < 0]) else 2200)

            net = max(0.0, income - expenses)
            projected = net * months_to_deadline
            shortfall = max(0.0, target_amount - projected)

            if shortfall == 0:
                score, status = 1.0, 'achievable'
            elif shortfall <= target_amount * 0.2:
                score, status = 0.75, 'achievable'
            elif shortfall <= target_amount * 0.5:
                score, status = 0.5, 'challenging'
            else:
                score, status = max(0.1, projected / target_amount), 'unrealistic'

            # Audit log if off-track (only if necessary)
            if status in ('challenging', 'unrealistic'):
                self.audit.log(
                    user_id=user_id,
                    decision_type='goal_warning',
                    severity='HIGH' if status == 'unrealistic' else 'MEDIUM',
                    trigger_reason=f'Goal {status}. Feasibility {score:.2f}. Shortfall ${shortfall:.2f}',
                    model_confidence_score=score,
                    data_validation_status=validation['status'],
                    model_used=self.name
                )

        return {
            'status': 'OK',
            'user_id': user_id,
            'feasibility_score': round(score, 2),
            'goal_status': status,
            'avg_monthly_income': round(income, 2),
            'avg_monthly_expenses': round(expenses, 2),
            'avg_monthly_net_savings': round(net, 2),
            'projected_savings': round(projected, 2),
            'projected_shortfall': round(shortfall, 2)
        }
