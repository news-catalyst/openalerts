from django.urls import path
from .views import (
    EmailSignUpView,
    EmailVerifyView,
    EmailSettingsView,
    EmailDeleteView,
    EmailDeleteConfirmView,
    IndexView
)

app_name = "public"

urlpatterns = [
    path("email/signup/", EmailSignUpView.as_view(extra_context={"title": "Email Sign Up"}), name="email_signup"),
    path("email/verify/<str:token>/", EmailVerifyView.as_view(extra_context={"title": "Email Verification"}), name="email_verify"),
    path("email/settings/<str:token>/", EmailSettingsView.as_view(extra_context={"title": "Email Settings"}), name="email_settings"),
    path("email/unsubscribe/confirm/", EmailDeleteConfirmView.as_view(extra_context={"title": "Email Unsubscribe"}), name="email_delete_confirm"),
    path("email/unsubscribe/<str:token>/", EmailDeleteView.as_view(extra_context={"title": "Email Unsubscribe Confirmed"}), name="email_delete"),
    path("", IndexView.as_view(), name="index")
]
