import pandas as pd
from datetime import datetime, timezone
import time

class FeedbackLog:
    def __init__(self):
        self.df = pd.DataFrame(columns=[
            'feedback_id','timestamp','user_id','model_type','prediction_id','original_prediction',
            'actual_outcome','feedback_type','user_explanation','model_confidence','corrected_value',
            'impact_score','action_taken','resolved','notes'
        ])

    def log(self, user_id, model_type, prediction_id, original_prediction,
            actual_outcome, feedback_type, user_explanation="",
            model_confidence=None, corrected_value=None):
        feedback_id = f"fb_{len(self.df):06d}_{int(time.time())}"
        impact_scores = {'correct':0.1,'incorrect':0.9,'partially_correct':0.5,'reasoning_unclear':0.4}
        impact = impact_scores.get(feedback_type,0.5)
        if model_confidence and feedback_type=='incorrect':
            impact = min(1.0, impact * (2.0 - model_confidence))
        row = pd.DataFrame([{
            'feedback_id': feedback_id,
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'user_id': user_id,
            'model_type': model_type,
            'prediction_id': prediction_id,
            'original_prediction': original_prediction,
            'actual_outcome': actual_outcome,
            'feedback_type': feedback_type,
            'user_explanation': user_explanation,
            'model_confidence': model_confidence,
            'corrected_value': corrected_value,
            'impact_score': impact,
            'action_taken': 'log_only',
            'resolved': False,
            'notes': ''
        }])
        self.df = pd.concat([self.df, row], ignore_index=True)
        return feedback_id

    def log_category(self, user_id, transaction_id, predicted_category, actual_category, model_confidence=None, transaction_features=None):
        explanation = f"Category misprediction: '{predicted_category}' → '{actual_category}'."
        if transaction_features:
            parts = []
            for k in ('amount','description','merchant'):
                if k in transaction_features:
                    v = transaction_features[k]
                    parts.append(f"{k}={v}")
            if parts:
                explanation += " (" + ", ".join(parts) + ")"
        return self.log(user_id,'category_classifier',transaction_id,predicted_category,actual_category,'incorrect',explanation,model_confidence,actual_category)

    def prepare_category_training(self, min_feedback_count=10):
        df = self.df[(self.df['model_type']=='category_classifier') & (self.df['feedback_type']=='incorrect') & (self.df['corrected_value'].notna())]
        if len(df) < min_feedback_count:
            return {'ready_for_training': False,'feedback_count': len(df),'min_required': min_feedback_count}
        examples = [{
            'transaction_id': r['prediction_id'],
            'incorrect_prediction': r['original_prediction'],
            'correct_label': r['corrected_value'],
            'model_confidence': r['model_confidence'],
            'impact_score': r['impact_score'],
            'timestamp': r['timestamp']
        } for _, r in df.iterrows()]
        pairs = (df['original_prediction'] + ' → ' + df['corrected_value']).value_counts().to_dict()
        return {
            'ready_for_training': True,
            'feedback_count': len(df),
            'training_examples': examples,
            'confusion_pairs': pairs,
            'avg_confidence_when_wrong': float(df['model_confidence'].mean()),
            'high_confidence_errors': int((df['model_confidence'] > 0.8).sum()),
        }
