from django.views.generic import TemplateView
from management.mixins import SessionAuthenticationRequiredMixin


class DashboardView(SessionAuthenticationRequiredMixin, TemplateView):
    template_name = "management/pages/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["organizations"] = self.request.session["organizations"]
        return context