from django.views.generic import TemplateView
from django.shortcuts import reverse, get_object_or_404
from public.mixins import OrganizationMixin
from alerts.models import Channel
from .email import EmailSignUpView

class EmbedMixin:
    def dispatch(self, request, *args, **kwargs):
        response = super(EmbedMixin, self).dispatch(request, *args, **kwargs)
        response["X-Frame-Options"] = None
        return response

class IndexEmbedView(OrganizationMixin, EmbedMixin, TemplateView):
    template_name = "public/embeds/index.html"

class EmailEmbedView(EmbedMixin, EmailSignUpView, OrganizationMixin):
    template_name = "public/embeds/email-signup.html"

    def get_success_url(self):
        return reverse("public:embed_email") + f"?org={self.get_context_data()['organization'].id}&success=True"

class LatestEmbedView(OrganizationMixin, EmbedMixin, TemplateView):
    template_name = "public/embeds/latest.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        alerts = data["organization"].alerts()[:3]
        if self.kwargs.get("channel", None) != None:
            alerts = get_object_or_404(Channel, id=self.kwargs.get("channel")).alerts[:3]
        data["alerts"] = alerts
        return data
            
