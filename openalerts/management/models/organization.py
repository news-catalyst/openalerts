from django.db import models
from django.shortcuts import reverse
import alerts

class Organization(models.Model):
    name = models.CharField(max_length=128)
    presspass_uuid = models.UUIDField(editable=False)
    website = models.URLField(blank=True, default='')
    description = models.TextField(blank=True, default='')
    primary_color = models.CharField(max_length=7, default="#444444", help_text="Your news organization's primary brand color.")
    logo_url = models.URLField(null=True, blank=True, help_text="The URL of your news organization's logo (for use on public facing pages).")

    @staticmethod
    def for_presspass_org(org):
        if not Organization.objects.filter(presspass_uuid=org["uuid"]).exists():
            return Organization.objects.create(name=org["name"], presspass_uuid=org["uuid"])
        return Organization.objects.get(presspass_uuid=org["uuid"])

    @staticmethod
    def for_session(session):
        orgs = []
        for org in session.get("presspass_organizations", []):
            orgs.append(Organization.for_presspass_org(org))
        return orgs

    def get_absolute_url(self):
        return reverse("management:organization", kwargs={"pk": self.pk})

    def channel_count(self):
        return self.channel_set.all().count()

    def subscriber_count(self):
        return sum(
            [self.emailsubscription_set.all().count()]
        )

    def alerts(self):
        return alerts.models.Alert.objects.filter(channel__organization=self).order_by("-published")

    
