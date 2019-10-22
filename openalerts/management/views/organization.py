from django.views.generic.edit import UpdateView
from management.mixins import SessionAuthenticationRequiredMixin, SessionOrgContextMixin
from management.models import Organization


class OrganizationView(
    SessionAuthenticationRequiredMixin, SessionOrgContextMixin, UpdateView
):
    template_name = "management/pages/organization.html"
    model = Organization
    fields = ["name", "website"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
