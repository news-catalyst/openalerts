from django.views.generic import TemplateView
from django.shortcuts import reverse
from public.mixins import OrganizationMixin

class IndexView(OrganizationMixin, TemplateView):
    template_name = "public/index.html"