from django.db import models
from .channel import Channel


class Alert(models.Model):
    channel = models.ForeignKey(
        Channel,
        on_delete=models.CASCADE,
        help_text="What channel does the alert belong to?",
    )
    content = models.TextField(
        help_text="What is the content of the alert? We recommend keeping this under 250 characters."
    )
    image_url = models.URLField(
        blank=True, editable=False
    )  # Not going to be implemented until its purpose is clearer
    url = models.URLField(
        blank=True,
        help_text="Where should subscribers go when they click on the alert? (Usually, this is the link to the associated news story on your website.)",
    )
    published = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
