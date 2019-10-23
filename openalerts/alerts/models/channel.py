from django.db import models

from management.models import Organization

class Channel(models.Model):
    name = models.CharField(max_length=128)
    organization = models.ForeignKey(Organization, editable=False, on_delete=models.CASCADE)
    slug = models.SlugField(auto_created=True, unique=True)
    description = models.TextField()
