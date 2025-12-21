import json
from pathlib import Path
from typing import Dict, Any, Optional

import numpy as np
import joblib


ARTIFACT_DIR = Path(__file__).resolve().parent.parent / 'model_store'
MANIFEST_FILE = ARTIFACT_DIR / 'artifact_manifest.json'


class AIModelService:
    def __init__(self):
        self.scaler = None
        self.label_encoder = None
        self.cat_encoder = None
        self.iso_forest = None
        self._loaded = False

    def load(self) -> bool:
        try:
            if MANIFEST_FILE.exists():
                manifest = json.loads(MANIFEST_FILE.read_text(encoding='utf-8'))
                def _load(name):
                    path = manifest.get(name)
                    if path:
                        return joblib.load(Path(path))
                    return None
                self.scaler = _load('scaler')
                self.label_encoder = _load('label_encoder')
                self.cat_encoder = _load('cat_encoder')
                self.iso_forest = _load('isolation_forest')
                self._loaded = any([self.scaler, self.label_encoder, self.cat_encoder, self.iso_forest])
                return self._loaded
            return False
        except Exception:
            return False

    def preprocess_transaction(self, tx: Dict[str, Any]) -> Dict[str, Any]:
        amount = float(tx.get('amount') or 0.0)
        category = tx.get('category_name') or tx.get('category') or 'Unknown'
        over_budget_pct = float(tx.get('over_budget_percentage') or 0.0)
        features = {
            'amount': amount,
            'over_budget_percentage': over_budget_pct,
            'category': category,
        }
        return features

    def predict_transaction(self, tx: Dict[str, Any]) -> Dict[str, Any]:
        f = self.preprocess_transaction(tx)
        x = np.array([[f['amount'], f['over_budget_percentage']]], dtype=float)
        anomaly_flag = 0
        anomaly_score = 0.0
        try:
            if self.iso_forest is not None:
                preds = self.iso_forest.predict(x)
                scores = self.iso_forest.score_samples(x)
                anomaly_flag = int(preds[0] == -1)
                anomaly_score = float(scores[0])
        except Exception:
            pass
        reason_parts = []
        if anomaly_flag:
            reason_parts.append(f"Behavioral Anomaly (score: {anomaly_score:.3f})")
        if f['over_budget_percentage'] > 100:
            reason_parts.append(f"Budget Overrun: {f['over_budget_percentage']:.0f}% over budget")
        reason = ' | '.join(reason_parts) if reason_parts else 'No anomaly detected'
        return {
            'is_fraud_flagged': anomaly_flag or (f['over_budget_percentage'] > 100),
            'anomaly_score': anomaly_score,
            'reason': reason,
            'features_used': f,
        }


_service_singleton: Optional[AIModelService] = None


def get_service() -> AIModelService:
    global _service_singleton
    if _service_singleton is None:
        svc = AIModelService()
        svc.load()
        _service_singleton = svc
    return _service_singleton
