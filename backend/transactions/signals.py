from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from .models import Transaction
from ai_alerts.models import AIAlert
from funder.ai_model_service import get_service


@receiver(post_save, sender=Transaction)
def run_ai_on_transaction(sender, instance: Transaction, created: bool, **kwargs):
    # Trigger on create only
    if not created:
        return
    try:
        svc = get_service()
        tx_dict = {
            'amount': float(instance.amount),
            'category_name': getattr(instance.category, 'name', None),
            'type': instance.type,
            'merchant': instance.merchant,
        }
        result = svc.predict_transaction(tx_dict)
        if result.get('is_fraud_flagged'):
            instance.flagged_fraud = True
            instance.save(update_fields=['flagged_fraud'])
            # Persist an alert tied to the user; include txn UUID in message for traceability
            txn_id = instance.get_uuid_string()
            msg = f"txn:{txn_id} | {result.get('reason')}"
            AIAlert.objects.create(
                user=instance.user,
                message=msg,
                type='FRAUD',
            )
    except Exception:
        # Non-blocking: do not break persistence if AI pipeline fails
        pass
