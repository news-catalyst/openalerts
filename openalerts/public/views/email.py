from django.views.generic import FormView
from django.shortcuts import reverse
from django.core.mail import send_mail
from django.conf import settings
from subscriptions.models import EmailSubscription
from public.mixins import OrganizationMixin
from public.forms import EmailSignupForm

class EmailSignUpView(OrganizationMixin, FormView):
    template_name = "public/email/signup.html"
    form_class = EmailSignupForm

    def get_success_url(self):
        return reverse("public:email_signup") + "?success=True"

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        subscription = EmailSubscription.objects.filter(email=email).first()
        if subscription == None:
            subscription = EmailSubscription.objects.create(
                email=email, organization=self.get_context_data()["organization"]
            )
        subscription.send_opt_in()
        return super(EmailSignUpView, self).form_valid(form)
        
