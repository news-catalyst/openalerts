from django.views.generic.base import ContextMixin
from management.models import Organization
from django.shortcuts import get_object_or_404

class OrganizationMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super(OrganizationMixin, self).get_context_data(**kwargs)
        if "org" in kwargs:
            context["organization"] = get_object_or_404(Organization, id=kwargs["org"])
        else:
            context["organzation"] = get_object_or_404(Organization, hostname=self.request.get_host())