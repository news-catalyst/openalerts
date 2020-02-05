from django.views.generic import FormView, RedirectView, TemplateView
from django.db import transaction
from django.views.generic.edit import UpdateView, DeleteView
from django.shortcuts import reverse, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from alerts.models import Alert, AlertStats
from ..mixins import OrganizationMixin
from ..tasks import increment_clicks


class UrlRedirectView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        alert = get_object_or_404(Alert, id=kwargs["id"])
        url = alert.url

        increment_clicks.delay(alert.pk, self.request.GET.get("S", "unknown"))

        if len(url.strip()) > 0:
            return url
        else:
            return (
                reverse("public:unknown_url") + f"?org={alert.channel.organization.id}"
            )


class UnknownUrlView(TemplateView, OrganizationMixin):
    """Displayed when the alert does not have any URL specified."""

    template_name = "public/unknown-url.html"
