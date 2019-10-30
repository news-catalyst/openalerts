from django.db.models.signals import post_save
from alerts.models import Alert
from management.models import Organization
from .models import EmailSubscriptionGroup, WebpushSubscription, WebpushSubscriptionGroup
from webpush.models import PushInformation

def on_alert_save(sender, instance, created, **kwargs):
    if created:
        # Send emails. TODO: do this in a backgrounded celery task
        EmailSubscriptionGroup.for_channel(instance.channel).push(instance)
        WebpushSubscriptionGroup.for_channel(instance.channel).push(instance)

post_save.connect(on_alert_save, sender=Alert)

# Detect new webpush subscribers
def on_webpush_save(sender, instance, created, **kwargs):
    if created:
        org = Organization.objects.get(id=instance.group.name)
        WebpushSubscription.objects.create(organization=org, subscription=instance)
        
post_save.connect(on_webpush_save, sender=PushInformation)