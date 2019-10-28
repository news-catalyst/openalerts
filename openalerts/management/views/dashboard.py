from django.views.generic import TemplateView
from management.mixins import SessionAuthenticationRequiredMixin, SessionOrgContextMixin
from django.shortcuts import redirect
from management.models import Organization

class DashboardView(SessionAuthenticationRequiredMixin, SessionOrgContextMixin, TemplateView):
    template_name = "management/pages/dashboard.html"

    def dispatch(self, *args, **kwargs):
        if len(self.get_context_data().get("organizations")) == 1:
            return redirect("management:organization", self.get_context_data().get("organizations")[0].id)
        return super(DashboardView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context