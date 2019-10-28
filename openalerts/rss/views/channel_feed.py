from django.contrib.syndication.views import Feed
from alerts.models import Channel

class ChannelFeed(Feed):
    def link(self, obj):
        return f"/rss/{obj.organization.id}/{obj.id}/" # TODO: show public channel web interface

    def title(self, obj):
        return f"{obj.name} by {obj.organization.name}"

    def description(self, obj):
        return obj.description

    def get_object(self, request, org_id, slug):
        return Channel.objects.get(organization__id=org_id, slug=slug)

    def items(self, obj):
        return obj.alerts[:15]

    def item_title(self, item):
        return f"Alert: " + item.channel.name # TODO: make configurable

    def item_description(self, item):
        return item.content

    def item_guid(self, item):
        return item.id

    def item_link(self, item):
        return item.url # TODO: fallback to frontend