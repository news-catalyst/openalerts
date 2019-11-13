from django.contrib import admin
from .models import Channel, Alert, Source

admin.site.register(Channel)
admin.site.register(Alert)
admin.site.register(Source)