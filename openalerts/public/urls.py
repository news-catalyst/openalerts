from django.urls import path
from .views import (
    EmailSignUpView
)

app_name = "public"

urlpatterns = [
    path("email/signup/", EmailSignUpView.as_view(), name="email_signup"),
]
