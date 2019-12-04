from django.views.generic.base import ContextMixin
from management.models import Organization
from django.shortcuts import get_object_or_404

class OrganizationMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super(OrganizationMixin, self).get_context_data(**kwargs)

        # Fallback to session-stored organization
        if "org" not in self.request.GET and "public_org" in self.request.session:
            context["organization"] = get_object_or_404(Organization, id=self.request.session.get("public_org"))
        elif "org" in self.request.GET:
            context["organization"] = get_object_or_404(Organization, id=self.request.GET.get("org"))
            self.request.session["public_org"] = context["organization"].id
        else:
            context["organization"] = get_object_or_404(Organization, custom_hostname=self.request.get_host())
        
        context["webpush"] = {
            "group": context["organization"].id
        }

        return context