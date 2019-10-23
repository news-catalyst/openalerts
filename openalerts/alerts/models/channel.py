from django.db import models
from django.utils.text import slugify
from management.models import Organization

class Channel(models.Model):
    name = models.CharField(max_length=128)
    organization = models.ForeignKey(Organization, editable=False, on_delete=models.CASCADE)
    slug = models.SlugField(editable=False)
    description = models.TextField()

    class Meta:
        unique_together = [["slug", "organization"]]

    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(value, allow_unicode=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
