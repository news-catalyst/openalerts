from django.urls import path
from .views import (
    DashboardView,
    OrganizationView,
    LoginView,
    LogoutView
)

app_name = "management"

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path("organization/<int:pk>/", OrganizationView.as_view(), name="organization"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]