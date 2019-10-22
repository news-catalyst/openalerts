from django.views.generic import TemplateView
from management.mixins import SessionAuthenticationRequiredMixin, SessionOrgContextMixin

from management.models import Organization

class DashboardView(SessionAuthenticationRequiredMixin, SessionOrgContextMixin, TemplateView):
    template_name = "management/pages/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context