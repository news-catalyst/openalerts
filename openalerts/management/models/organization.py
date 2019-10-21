from django.db import models


class Organization(models.Model):
    name = models.CharField(max_length=128)
    presspass_uuid = models.UUIDField()
    website = models.URLField()
