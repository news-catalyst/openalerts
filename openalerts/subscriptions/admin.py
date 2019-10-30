from django.contrib import admin
from .models import EmailSubscription, WebpushSubscription

admin.site.register(EmailSubscription)
admin.site.register(WebpushSubscription)