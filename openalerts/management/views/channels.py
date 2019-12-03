from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.base import ContextMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from management.mixins import SessionAuthenticationRequiredMixin, SessionOrgContextMixin, OrgContextMixin
from management.models import Organization
from alerts.models import Channel, Alert
from django.utils.http import urlencode

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
        return reverse_lazy("management:channel", kwargs={"org_id": self.kwargs["org_id"], "pk": self.object.id})

class EditChannelView(
    SessionAuthenticationRequiredMixin, SessionOrgContextMixin, OrgContextMixin, UpdateView
):
    template_name = "management/pages/edit_channel.html"
    model = Channel
    fields = ["name", "description"]

    def get_success_url(self, **kwargs):
        return reverse_lazy("management:channel", kwargs={"org_id": self.kwargs["org_id"], "pk": self.object.id})

class DeleteChannelView(
    SessionAuthenticationRequiredMixin, SessionOrgContextMixin, OrgContextMixin, DeleteView
):
    template_name = "management/pages/delete_channel.html"
    model = Channel

    def get_success_url(self, **kwargs):
        return reverse_lazy("management:channel_list", kwargs={"org_id": self.kwargs["org_id"]})

class ChannelView(
    SessionAuthenticationRequiredMixin, SessionOrgContextMixin, OrgContextMixin, DetailView
):
    template_name = "management/pages/channel.html"
    model = Channel

    def get_context_data(self, **kwargs):
        search = self.request.GET.get("search", None)
        objects = self.object.alerts
        if search:
            objects = self.object.alerts.filter(content__icontains=search)
        paginator = Paginator(objects, 15)
        page_obj = paginator.get_page(self.request.GET.get("page", 1))
        context = super(ChannelView, self).get_context_data(**kwargs)
        context.update(dict(page_obj=page_obj, paginator=paginator, total_alerts=objects.count(), url_parameters=urlencode([("search", search)])))
        return context
