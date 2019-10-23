from django.urls import path
from .views import (
    DashboardView,
    OrganizationView,
    LoginView,
    LogoutView,
    ChannelListView,
    ChannelView,
    CreateChannelView
)

app_name = "management"

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path("organization/<int:pk>/", OrganizationView.as_view(), name="organization"),
    path("organization/<int:org_id>/channels/", ChannelListView.as_view(), name="channel_list"),
    path("organization/<int:org_id>/channels/create/", CreateChannelView.as_view(), name="create_channel"),
    path("organization/<int:org_id>/channels/<int:pk>/", ChannelView.as_view(), name="channel"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]