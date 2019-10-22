from django.views.generic import TemplateView
from management.mixins import SessionAuthenticationRequiredMixin

from management.models import Organization

class DashboardView(SessionAuthenticationRequiredMixin, TemplateView):
    template_name = "management/pages/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["organizations"] = Organization.for_session(self.request.session)
        return context