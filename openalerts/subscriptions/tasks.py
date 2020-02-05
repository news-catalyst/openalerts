from celery import shared_task
from django.db import transaction

from alerts.models import Alert
from subscriptions.models import EmailSubscriptionGroup, WebpushSubscriptionGroup

@shared_task
def publish_alert(alert_pk):
    alert = Alert.objects.get(pk=alert_pk)
    EmailSubscriptionGroup.for_channel(alert.channel).push(alert)
    WebpushSubscriptionGroup.for_channel(alert.channel).push(alert)