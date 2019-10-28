from django.urls import path
from .views import ChannelFeed

app_name = "rss"

urlpatterns = [path("<int:org_id>/<str:slug>/", ChannelFeed(), name="channel_feed")]
