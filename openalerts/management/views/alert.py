from django.views.generic.edit import CreateView
from management.mixins import SessionAuthenticationRequiredMixin, SessionOrgContextMixin, OrgContextMixin
from django.urls import reverse
from management.models import Organization
from alerts.models import Channel, Alert

class CreateAlertView(SessionAuthenticationRequiredMixin, SessionOrgContextMixin, OrgContextMixin, CreateView):
    template_name = "management/pages/edit_alert.html"
    model = Alert
    fields = ["channel", "content", "url", "image_url"]

    def get_form(self, *args, **kwargs):
        form = super(CreateAlertView, self).get_form(*args, **kwargs)
        form.fields['channel'].queryset = Channel.objects.filter(organization__id=self.kwargs["org_id"])
        return form

    def get_initial(self):
        initial = super().get_initial()
        if self.request.GET.get("channel", None) != None:
            initial["channel"] = int(self.request.GET.get("channel"))
        return initial

    def get_success_url(self):
        return reverse("management:channel", args={"org_id": self.object.organization.id, "pk": self.object.pk})