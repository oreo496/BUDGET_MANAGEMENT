from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import datetime

from .models import Goal
from ai_alerts.models import AIAlert


@receiver(post_save, sender=Goal)
def analyze_goal_on_create(sender, instance: Goal, created: bool, **kwargs):
    if not created:
        return
    try:
        # Basic feasibility estimation similar to the notebook's intent
        target = float(instance.target_amount)
        current = float(instance.current_amount)
        months_remaining = 6
        if instance.deadline:
            try:
                dl = datetime.combine(instance.deadline, datetime.min.time()).replace(tzinfo=timezone.utc)
                months_remaining = max(1, int((dl - timezone.now()).days / 30))
            except Exception:
                months_remaining = 6
        projected_total = current  # Without income history, assume no future contributions
        shortfall = max(0.0, target - projected_total)
        status = 'on_track' if shortfall == 0 else ('challenging' if shortfall <= target * 0.5 else 'unrealistic')
        msg = (
            f"Goal '{instance.title}' status: {status}. Shortfall ${shortfall:.2f}. "
            f"Months remaining: {months_remaining}."
        )
        AIAlert.objects.create(
            user=instance.user,
            message=msg,
            type='GOAL_RECOMMENDATION',
        )
    except Exception:
        pass
