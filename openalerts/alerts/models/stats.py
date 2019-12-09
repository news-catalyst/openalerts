from django.db import models
from .alert import Alert

class AlertStats(models.Model):
    alert = models.OneToOneField(Alert, on_delete=models.CASCADE)

    webpush_sends = models.BigIntegerField(default=0)
    webpush_clicks = models.BigIntegerField(default=0)

    email_sends = models.BigIntegerField(default=0)
    email_clicks = models.BigIntegerField(default=0)

    other_clicks = models.BigIntegerField(default=0)

    @staticmethod
    def for_alert(alert: Alert):
        filtered = AlertStats.objects.filter(alert=alert)
        if filtered.exists():
            return filtered.first()
        else:
            return AlertStats.objects.create(alert=alert)

    @staticmethod
    def for_alert_locking(alert: Alert):
        filtered = AlertStats.objects.filter(alert=alert)
        if not filtered.exists():
            AlertStats.objects.create(alert=alert)
        return AlertStats.objects.select_for_update().get(alert=alert)
