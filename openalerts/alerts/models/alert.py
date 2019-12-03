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

    def get_public_url(self):
        return reverse("public:url_redirect", kwargs={
            "id": self.pk
        })
