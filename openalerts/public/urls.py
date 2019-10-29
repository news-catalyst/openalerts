from django.urls import path
from .views import (
    EmailSignUpView,
    EmailVerifyView,
    EmailSettingsView,
    EmailDeleteView,
    EmailDeleteConfirmView,
)

app_name = "public"

urlpatterns = [
    path("email/signup/", EmailSignUpView.as_view(), name="email_signup"),
    path("email/verify/<str:token>/", EmailVerifyView.as_view(), name="email_verify"),
    path("email/settings/<str:token>/", EmailSettingsView.as_view(), name="email_settings"),
    path("email/unsubscribe/confirm/", EmailDeleteConfirmView.as_view(), name="email_delete_confirm"),
    path("email/unsubscribe/<str:token>/", EmailDeleteView.as_view(), name="email_delete"),
]
