from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.base import ContextMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from management.mixins import SessionAuthenticationRequiredMixin, SessionOrgContextMixin
from management.models import Organization
from alerts.models import Channel

class OrgContextMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super(OrgContextMixin, self).get_context_data(**kwargs)
        context.update(dict(organization=Organization.objects.get(id=self.kwargs["org_id"])))
        return context

class ChannelListView(
    SessionAuthenticationRequiredMixin, SessionOrgContextMixin, DetailView
):
    template_name = "management/pages/channel_list.html"
    model = Organization
    pk_url_kwarg = "org_id"    

class CreateChannelView(
    SessionAuthenticationRequiredMixin, SessionOrgContextMixin, OrgContextMixin, CreateView
):
    template_name = "management/pages/edit_channel.html"
    model = Channel
    fields = ["name", "description"]

    def form_valid(self, form):
        form.instance.organization = self.get_context_data()["organization"]
        return super(CreateChannelView, self).form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse_lazy("management:channel_list", args={"org_id": self.kwargs["org_id"]})

class ChannelView(
    SessionAuthenticationRequiredMixin, SessionOrgContextMixin, OrgContextMixin, DetailView
):
    template_name = "management/pages/channel.html"
    model = Channel
