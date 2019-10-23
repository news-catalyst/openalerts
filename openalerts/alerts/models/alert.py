from django.db import models
from .channel import Channel

class Alert(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    content = models.TextField()
    image_url = models.URLField(blank=True)
    url = models.URLField(blank=True)
    posted = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)