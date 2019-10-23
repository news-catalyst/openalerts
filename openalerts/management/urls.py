from django.urls import path
from .views import (
    DashboardView,
    OrganizationView,
    LoginView,
    LogoutView,
    ChannelsView,
    ChannelView
)

app_name = "management"

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path("organization/<int:pk>/", OrganizationView.as_view(), name="organization"),
    path("organization/<int:pk>/channels/", ChannelsView.as_view(), name="channels"),
    path("organization/<int:org_id>/channels/<int:pk>/", ChannelView.as_view(), name="channel"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]