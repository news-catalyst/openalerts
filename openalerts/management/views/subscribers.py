from django.shortcuts import get_object_or_404, reverse
from django.views.generic import TemplateView, View
from django.conf import settings
from datetime import timedelta, datetime
from django import forms
from django.http import HttpResponse
import io
import unicodecsv as csv
from management.mixins import (
    SessionAuthenticationRequiredMixin,
    SessionOrgContextMixin,
    OrgContextMixin,
)
from management.models import Organization
from subscriptions.models import WebpushSubscription, EmailSubscription


class SubscriberTableView(
    SessionAuthenticationRequiredMixin, OrgContextMixin, TemplateView
):
    template_name = "management/pages/subscribers.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["email_subscribers"] = EmailSubscription.objects.filter(
            organization=data["organization"]
        )
        data["webpush_subscribers"] = WebpushSubscription.objects.filter(
            organization=data["organization"]
        )
        return data


class SubscriberEmailExportView(
    SessionAuthenticationRequiredMixin, OrgContextMixin, View
):
    def get(self, request, *args, **kwargs):
        org = request.organization

        outfile = io.BytesIO()
        writer = csv.DictWriter(
            outfile, fieldnames=["email", "verified", "created", "channels"]
        )
        writer.writeheader()
        writer.writerows(
            [
                {
                    "email": sub.email,
                    "verified": sub.verified,
                    "created": sub.created,
                    "channels": ", ".join(
                        [channel.name for channel in sub.channels.all()]
                    ),
                }
                for sub in EmailSubscription.objects.filter(organization=org)
            ]
        )

        response = HttpResponse(outfile.getvalue(), content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="OA_EmailExport.csv"'
        return response
