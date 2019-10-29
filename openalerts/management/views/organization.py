from django.views.generic.edit import UpdateView
from django.views.generic.detail import DetailView
from management.mixins import SessionAuthenticationRequiredMixin, SessionOrgContextMixin, OrgContextMixin
from management.models import Organization


class EditOrganizationView(
    SessionAuthenticationRequiredMixin, SessionOrgContextMixin, UpdateView
):
    template_name = "management/pages/edit_organization.html"
    model = Organization
    fields = ["name", "website", "description"]
    pk_url_kwarg = "org_id"

class OrganizationView(
    SessionAuthenticationRequiredMixin, SessionOrgContextMixin, DetailView
):
    template_name = "management/pages/organization.html"
    model = Organization
    pk_url_kwarg = "org_id"