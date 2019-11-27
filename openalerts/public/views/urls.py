from django.views.generic import FormView, RedirectView, TemplateView
from django.views.generic.edit import UpdateView, DeleteView
from django.shortcuts import reverse, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from alerts.models import Alert
from ..mixins import OrganizationMixin

class UrlRedirectView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        alert = get_object_or_404(Alert, id=kwargs["id"])
        url = alert.url
        if len(url.strip()) > 0:
            return url
        else:
            return reverse("public:unknown_url") + f"?org={alert.channel.organization.id}"

class UnknownUrlView(TemplateView, OrganizationMixin):
    """Displayed when the alert does not have any URL specified."""
    template_name = "public/unknown-url.html"