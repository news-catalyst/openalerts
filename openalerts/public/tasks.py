from celery import shared_task
from django.db import transaction

from alerts.models import Alert, AlertStats

@shared_task
def increment_clicks(alert_pk, source):
    with transaction.atomic():
        alert = Alert.objects.get(pk=alert_pk)
        stats = AlertStats.for_alert_locking(alert)
        if source == "em":
            stats.email_clicks += 1
        elif source == "wp":
            stats.webpush_clicks += 1
        else:
            stats.other_clicks += 1
        stats.save()