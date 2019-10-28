from django.contrib.syndication.views import Feed
from management.models import Organization
from alerts.models import Alert

class OrganizationFeed(Feed):
    def link(self, obj):
        return f"/rss/{obj.id}/" # TODO: show public channel web interface

    def title(self, obj):
        return f"{obj.name}"

    def description(self, obj):
        return f"All alerts and notifications published by {obj.name}" # TODO: make configurable

    def get_object(self, request, org_id):
        return Organization.objects.get(id=org_id)

    def items(self, obj):
        return Alert.objects.filter(channel__organization=obj).order_by("-published")[:15]

    def item_title(self, item):
        return f"Alert: " + item.channel.name # TODO: make configurable

    def item_description(self, item):
        return item.content

    def item_guid(self, item):
        return item.id

    def item_link(self, item):
        return item.url # TODO: fallback to frontend