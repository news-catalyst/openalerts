from django.db.models.signals import post_save
from alerts.models import Alert
from .models import EmailSubscriptionGroup

def on_alert_save(sender, instance, created, **kwargs):
    if created:
        # Send emails
        EmailSubscriptionGroup.for_channel(instance.channel).push(instance)

post_save.connect(on_alert_save, sender=Alert)