from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect
from django.views.generic.base import ContextMixin

from management.models import Organization

class SessionAuthenticationRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated."""
    def dispatch(self, request, *args, **kwargs):
        if not request.session.get("presspass_authenticated", False) == True:
            return redirect("management:login")
        return super().dispatch(request, *args, **kwargs)

class SessionOrgContextMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super(SessionOrgContextMixin, self).get_context_data(**kwargs)
        context.update(dict(organizations=Organization.for_session(self.request.session)))
        return context

class OrgContextMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super(OrgContextMixin, self).get_context_data(**kwargs)
        context.update(dict(organization=Organization.objects.get(id=self.kwargs["org_id"])))
        return context