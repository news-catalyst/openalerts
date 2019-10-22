from django.db import models
from django.shortcuts import reverse

class Organization(models.Model):
    name = models.CharField(max_length=128)
    presspass_uuid = models.UUIDField(editable=False)
    website = models.URLField(blank=True, default='')

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
    
