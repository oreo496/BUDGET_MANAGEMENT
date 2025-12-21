import pandas as pd
from datetime import datetime, timezone
import time

class AuditLogger:
    def __init__(self):
        self.df = pd.DataFrame(columns=[
            'audit_id','timestamp','user_id','decision_type','severity','trigger_reason',
            'model_confidence_score','affected_transaction_id','affected_amount','affected_category',
            'data_validation_status','model_used','admin_action_taken','resolution_notes','resolved'
        ])

    def log(self, user_id, decision_type, severity, trigger_reason,
            model_confidence_score=None, affected_transaction_id=None,
            affected_amount=None, affected_category=None, data_validation_status=None,
            model_used=None):
        audit_id = f"audit_{len(self.df):08d}_{int(time.time())}"
        new_row = pd.DataFrame([{
            'audit_id': audit_id,
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'user_id': user_id,
            'decision_type': decision_type,
            'severity': severity,
            'trigger_reason': trigger_reason,
            'model_confidence_score': model_confidence_score,
            'affected_transaction_id': affected_transaction_id,
            'affected_amount': affected_amount,
            'affected_category': affected_category,
            'data_validation_status': data_validation_status,
            'model_used': model_used,
            'admin_action_taken': 'pending',
            'resolution_notes': '',
            'resolved': False
        }])
        self.df = pd.concat([self.df, new_row], ignore_index=True)
        return audit_id
