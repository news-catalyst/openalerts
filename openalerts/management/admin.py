from django.contrib import admin

from .models import Organization

class OrganizationAdmin(admin.ModelAdmin):
    list_display = ["name", "presspass_uuid", "website"]

admin.site.register(Organization, OrganizationAdmin)