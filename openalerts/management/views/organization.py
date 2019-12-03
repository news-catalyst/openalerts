from django.views.generic.edit import UpdateView
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404, reverse
from django import forms
from management.mixins import SessionAuthenticationRequiredMixin, SessionOrgContextMixin, OrgContextMixin
from management.models import Organization


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