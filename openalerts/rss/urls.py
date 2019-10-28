from django.urls import path
from .views import ChannelFeed, OrganizationFeed

app_name = "rss"

urlpatterns = [
    path("<int:org_id>/<str:slug>/", ChannelFeed(), name="channel_feed"),
    path("<int:org_id>/", OrganizationFeed(), name="organization_feed"),
]
