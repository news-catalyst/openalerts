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
    CreateAlertView,
    EditAlertView,
    DeleteAlertView,
    DeleteChannelView,
    SourceListView,
    DeleteSourceView,
    CreateSourceView,
    OrganizationIntegrationsView,
    SubscriberTableView,
    SubscriberEmailExportView
)

app_name = "management"

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path(
        "organization/<int:org_id>/",
        OrganizationView.as_view(extra_context={"tab_scope": "overview"}),
        name="organization",
    ),
    path(
        "organization/<int:org_id>/integrations/",
        OrganizationIntegrationsView.as_view(extra_context={"tab_scope": "overview"}),
        name="integrations",
    ),
    path(
        "organization/<int:org_id>/edit/",
        EditOrganizationView.as_view(extra_context={"tab_scope": "overview"}),
        name="edit_organization",
    ),
    path(
        "organization/<int:org_id>/channels/",
        ChannelListView.as_view(extra_context={"tab_scope": "channels"}),
        name="channel_list",
    ),
    path(
        "organization/<int:org_id>/channels/create/",
        CreateChannelView.as_view(extra_context={"tab_scope": "channels"}),
        name="create_channel",
    ),
    path(
        "organization/<int:org_id>/channels/<int:pk>/",
        ChannelView.as_view(extra_context={"tab_scope": "channels"}),
        name="channel",
    ),
    path(
        "organization/<int:org_id>/channels/<int:pk>/edit/",
        EditChannelView.as_view(extra_context={"tab_scope": "channels"}),
        name="edit_channel",
    ),
    path(
        "organization/<int:org_id>/channels/<int:pk>/delete/",
        DeleteChannelView.as_view(extra_context={"tab_scope": "channels"}),
        name="delete_channel",
    ),
    path(
        "organization/<int:org_id>/channels/<int:channel_id>/sources/",
        SourceListView.as_view(extra_context={"tab_scope": "channels"}),
        name="source_list"
    ),
    path(
        "organization/<int:org_id>/channels/<int:channel_id>/sources/create/",
        CreateSourceView.as_view(extra_context={"tab_scope": "channels"}),
        name="create_source"
    ),
    path(
        "organization/<int:org_id>/channels/<int:channel_id>/sources/<int:pk>/delete/",
        DeleteSourceView.as_view(extra_context={"tab_scope": "channels"}),
        name="delete_source"
    ),
    path(
        "organization/<int:org_id>/alert/publish/",
        CreateAlertView.as_view(extra_context={"tab_scope": "publish"}),
        name="create_alert",
    ),
    path(
        "organization/<int:org_id>/alert/<int:pk>/edit/",
        EditAlertView.as_view(extra_context={"tab_scope": "publish"}),
        name="edit_alert",
    ),
    path(
        "organization/<int:org_id>/alert/<int:pk>/delete/",
        DeleteAlertView.as_view(extra_context={"tab_scope": "publish"}),
        name="delete_alert",
    ),
    path(
        "organization/<int:org_id>/subscribers/",
        SubscriberTableView.as_view(extra_context={"tab_scope": "subscribers"}),
        name="subscribers"
    ),
    path(
        "organization/<int:org_id>/subscribers/export/",
        SubscriberEmailExportView.as_view(extra_context={"tab_scope": "subscribers"}),
        name="subscribers_email_export"
    ),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
