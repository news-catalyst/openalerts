from django.urls import path
from .views import (
    DashboardView,
    OrganizationView,
    EditOrganizationView,
    LoginView,
    LogoutView,
    ChannelListView,
    ChannelView,
    CreateChannelView,
    EditChannelView,
    CreateAlertView
)

app_name = "management"

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path("organization/<int:pk>/", OrganizationView.as_view(extra_context={"tab_scope": "overview"}), name="organization"),
    path("organization/<int:pk>/edit/", EditOrganizationView.as_view(extra_context={"tab_scope": "overview"}), name="edit_organization"),
    path("organization/<int:org_id>/channels/", ChannelListView.as_view(extra_context={"tab_scope": "channels"}), name="channel_list"),
    path("organization/<int:org_id>/channels/create/", CreateChannelView.as_view(extra_context={"tab_scope": "channels"}), name="create_channel"),
    path("organization/<int:org_id>/channels/<int:pk>/", ChannelView.as_view(extra_context={"tab_scope": "channels"}), name="channel"),
    path("organization/<int:org_id>/channels/<int:pk>/edit/", EditChannelView.as_view(extra_context={"tab_scope": "channels"}), name="edit_channel"),
    path("organization/<int:org_id>/publish/", CreateAlertView.as_view(extra_context={"tab_scope": "publish"}), name="create_alert"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]