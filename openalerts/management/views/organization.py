from django.views.generic.edit import UpdateView
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404, reverse
from django.utils import timezone
from datetime import timedelta, datetime
from django import forms
from management.mixins import SessionAuthenticationRequiredMixin, SessionOrgContextMixin, OrgContextMixin
from management.models import Organization
from subscriptions.models import WebpushSubscription, EmailSubscription


class EditOrganizationView(
    SessionAuthenticationRequiredMixin, SessionOrgContextMixin, UpdateView
):
    template_name = "management/pages/edit_organization.html"
    model = Organization
    fields = ["name", "website", "description", "logo_url", "primary_color", "head_inject"]
    pk_url_kwarg = "org_id"

    def get_form(self, *args, **kwargs):
        form = super(EditOrganizationView, self).get_form(*args, **kwargs)
        form["primary_color"].field.widget.input_type = "color"
        return form
    
    def get_object(self):
        return get_object_or_404(Organization, id=self.kwargs["org_id"])

    def get_success_url(self):
        print(self.object.id)
        return reverse("management:organization", args=[self.object.id])

class OrganizationView(
    SessionAuthenticationRequiredMixin, SessionOrgContextMixin, DetailView
):
    template_name = "management/pages/organization.html"
    model = Organization
    pk_url_kwarg = "org_id"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        email_subscribers = EmailSubscription.objects.filter(organization=self.object)
        webpush_subscribers = WebpushSubscription.objects.filter(organization=self.object)

        data["subscribers"] = {
            "keys": str(["Email", "Web Alerts"]),
            "values": str([email_subscribers.count(),
                           webpush_subscribers.count()]),
            "count": email_subscribers.count() + webpush_subscribers.count(),
        }

        subscribers = list(email_subscribers) + list(webpush_subscribers)
        times = reversed([timezone.now() - timedelta(n) for n in range(90)]) # last 90 days

        data["subscribers_timeseries"] = {
            "label": "Currently Active Subscribers",
            "values": str([{
                "t": time.isoformat(),
                "y": len([subscription for subscription in subscribers if subscription.created <= time])
                # Deleted subscribers will not be shown in the chart, hence "current"
            } for time in times])
        }

        print(data["subscribers_timeseries"])

        return data