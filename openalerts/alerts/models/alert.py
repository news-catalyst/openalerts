from django.db import models
from django.shortcuts import reverse
from .channel import Channel
from .source import Source

class Alert(models.Model):
    channel = models.ForeignKey(
        Channel,
        on_delete=models.CASCADE,
        help_text="What channel does the alert belong to?",
    )
    content = models.TextField(
        help_text="What is the content of the alert? We recommend keeping this under 250 characters.",
        db_index=True
    )
    image_url = models.URLField(
        blank=True, editable=False
    )  # Not going to be implemented until its purpose is clearer
    url = models.URLField(
        blank=True,
        help_text="Where should subscribers go when they click on the alert? (Usually, this is the link to the associated news story on your website.)",
        db_index=True
    )
    published = models.DateTimeField(auto_now_add=True, db_index=True)
    updated = models.DateTimeField(auto_now=True)
    source = models.ForeignKey(Source, on_delete=models.SET_NULL, null=True)
    source_identifier = models.TextField(null=True) # Because null != null, this does not violate unique constraint

    class Meta:
        unique_together = ('source', 'source_identifier')

    def get_public_url(self, source):
        return reverse("public:url_redirect", kwargs={
            "id": self.pk
        }) + "?s=" + source

    @property
    def stats(self):
        return AlertStats.for_alert(self)

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

    def total_distribution(self):
        return self.webpush_sends + self.email_sends

    def total_clicks(self):
        return self.other_clicks + self.webpush_clicks + self.email_clicks

    def total_ctr(self):
        return 100.0 * self.total_clicks() / max([self.total_distribution(), 1])

    def webpush_ctr(self):
        return 100.0 * self.webpush_clicks / max([self.webpush_sends, 1])

    def email_ctr(self):
        return 100.0 * self.email_clicks / max([self.email_sends, 1])

    def relative_ctr(self):
        if not hasattr(self, "_relative_ctr") or self._relative_ctr == None: # Caching
            surrounding_alerts = Alert.objects.filter(channel=self.alert.channel, published__lt=self.alert.published).order_by("-published")[:25]
            # this is somewhat inefficient; it could be worth finding a few good ways to optimize this function
            avg_ctr = sum([alert.stats.total_ctr() for alert in surrounding_alerts])/max([1, len(surrounding_alerts)])
            self._relative_ctr = self.total_ctr() - avg_ctr
        return self._relative_ctr

    def click_stats(self):
        return {
            "keys": ["Email", "Notifications", "Other"],
            "values": [self.email_clicks, self.webpush_clicks, self.other_clicks],
            "count": self.total_clicks()
        }