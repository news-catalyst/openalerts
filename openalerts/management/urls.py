from django.urls import path
from .views import (
    DashboardView,
    LoginView
)

app_name = "management"

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path("login/", LoginView.as_view(), name="login"),
]