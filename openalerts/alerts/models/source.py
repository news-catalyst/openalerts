from django.db import models
from .channel import Channel

class Source(models.Model):
    source = models.CharField(max_length=10, choices=[("TWITTER", "Twitter")])
    identifier = models.TextField() # In the case of Twitter, the account's username/ID
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("source", "identifier")