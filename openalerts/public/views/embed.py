from django.views.generic import TemplateView
from django.shortcuts import reverse
from public.mixins import OrganizationMixin

class EmbedMixin:
    def dispatch(self, request, *args, **kwargs):
        response = super(EmbedMixin, self).dispatch(request, *args, **kwargs)
        response["X-Frame-Options"] = None
        return response

class IndexEmbedView(OrganizationMixin, EmbedMixin, TemplateView):
    template_name = "public/embeds/index.html"