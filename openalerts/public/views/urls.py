from django.views.generic import FormView, RedirectView, TemplateView
from django.db import transaction
from django.views.generic.edit import UpdateView, DeleteView
from django.shortcuts import reverse, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from alerts.models import Alert, AlertStats
from ..mixins import OrganizationMixin


class UrlRedirectView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        alert = get_object_or_404(Alert, id=kwargs["id"])
        url = alert.url

        with transaction.atomic():  # XXX: do in task queue to reduce user's exposure to db latency
            stats = AlertStats.for_alert_locking(alert)
            source = self.request.GET.get("s", "unknown")
            if source == "em":
                stats.email_clicks += 1
            elif source == "wp":
                stats.webpush_clicks += 1
            else:
                stats.other_clicks += 1
            stats.save()

        if len(url.strip()) > 0:
            return url
        else:
            return (
                reverse("public:unknown_url") + f"?org={alert.channel.organization.id}"
            )


class UnknownUrlView(TemplateView, OrganizationMixin):
    """Displayed when the alert does not have any URL specified."""

    template_name = "public/unknown-url.html"
