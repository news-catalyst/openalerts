from django.db import models
from .channel import Channel

class Source(models.Model):
    source = models.CharField(max_length=10, choices=[("TWITTER", "Twitter")])
    identifier = models.TextField(null=True, blank=True) # In the case of Twitter, the account's ID
    human_readable_identifier = models.TextField(blank=True, default="") # In the case of Twitter, the account's screen name
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("source", "identifier")

    def save(self, *args, **kwargs):
        if len(self.identifier.strip()) == 0:
            self.identifier = None
        super(Source, self).save(*args, **kwargs)

    def __str__(self):
        return self.human_readable_identifier