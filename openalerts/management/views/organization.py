from django.views.generic.edit import UpdateView
from django.views.generic.detail import DetailView
from management.mixins import SessionAuthenticationRequiredMixin, SessionOrgContextMixin
from management.models import Organization


class EditOrganizationView(
    SessionAuthenticationRequiredMixin, SessionOrgContextMixin, SessionOrgPermRequiredMixin, UpdateView
):
    template_name = "management/pages/edit_organization.html"
    model = Organization
    fields = ["name", "website", "description"]

class OrganizationView(
    SessionAuthenticationRequiredMixin, SessionOrgContextMixin, SessionOrgPermRequiredMixin, DetailView
):
    template_name = "management/pages/organization.html"
    model = Organization