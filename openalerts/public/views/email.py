from django.views.generic import FormView, RedirectView, TemplateView
from django.views.generic.edit import UpdateView, DeleteView
from django.shortcuts import reverse
from django.core.mail import send_mail
from django.conf import settings
from subscriptions.models import EmailSubscription
from public.mixins import OrganizationMixin
from public.forms import EmailSignupForm, EmailSettingsForm


class EmailSignUpView(OrganizationMixin, FormView):
    template_name = "public/email/signup.html"
    form_class = EmailSignupForm

    def get_success_url(self):
        return reverse("public:email_signup") + "?success=True"

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        organization = self.get_context_data()["organization"]
        subscription = EmailSubscription.objects.filter(email=email).first()
        if subscription == None:
            subscription = EmailSubscription.objects.create(
                email=email, organization=organization
            )
            for channel in organization.channel_set.all():
                # By default, they are subscribed to all channels
                subscription.channels.add(channel)
        subscription.send_opt_in()
        return super(EmailSignUpView, self).form_valid(form)


class EmailVerifyView(OrganizationMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        token = self.kwargs["token"]
        subscription = EmailSubscription.activate_verification_token(token)
        return reverse("public:email_settings", args=[subscription.get_access_token()]) + "?verified=True"


class EmailSettingsView(OrganizationMixin, UpdateView):
    template_name = "public/email/settings.html"
    form_class = EmailSettingsForm
    model = EmailSubscription

    def get_object(self, *args, **kwargs):
        return EmailSubscription.for_access_token(self.kwargs["token"])

    def get_success_url(self):
        return reverse("public:email_settings", args=[self.kwargs["token"]]) + "?success=True"


class EmailDeleteView(OrganizationMixin, DeleteView):
    template_name = "public/email/delete.html"
    model = EmailSubscription

    def get_object(self, *args, **kwargs):
        return EmailSubscription.for_access_token(self.kwargs["token"])

    def get_success_url(self):
        return reverse("public:email_delete_confirm")


class EmailDeleteConfirmView(OrganizationMixin, TemplateView):
    template_name = "public/email/delete-confirm.html"
