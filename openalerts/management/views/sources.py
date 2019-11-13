from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.base import ContextMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django import forms
from django.core.paginator import Paginator
from management.mixins import (
    SessionAuthenticationRequiredMixin,
    SessionOrgContextMixin,
    OrgContextMixin,
)
from management.models import Organization
from alerts.models import Source, Channel


class SourceListView(
    SessionAuthenticationRequiredMixin, SessionOrgContextMixin, OrgContextMixin, DetailView
):
    template_name = "management/pages/source_list.html"
    model = Channel
    pk_url_kwarg = "channel_id"


class CreateSourceView(
    SessionAuthenticationRequiredMixin,
    SessionOrgContextMixin,
    OrgContextMixin,
    CreateView,
):
    template_name = "management/pages/edit_source.html"
    model = Source
    fields = ["source", "human_readable_identifier"]

    def get_form(self, *args, **kwargs):
        form = super(CreateSourceView, self).get_form(*args, **kwargs)
        form.fields['human_readable_identifier'].label = "Username or handle"
        form.fields['human_readable_identifier'].widget = forms.TextInput()
        return form

    def get_context_data(self, **kwargs):
        context = super(CreateSourceView, self).get_context_data(**kwargs)
        context.update(dict(channel=Channel.objects.get(id=self.kwargs["channel_id"])))
        return context

    def form_valid(self, form):
        form.instance.channel = self.get_context_data()["channel"]
        return super(CreateSourceView, self).form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse_lazy(
            "management:source_list",
            kwargs={
                "org_id": self.kwargs["org_id"],
                "channel_id": self.object.channel.id,
            },
        )


class DeleteSourceView(
    SessionAuthenticationRequiredMixin,
    SessionOrgContextMixin,
    OrgContextMixin,
    DeleteView,
):
    template_name = "management/pages/delete_source.html"
    model = Source

    def get_success_url(self, **kwargs):
        return reverse_lazy(
            "management:source_list",
            kwargs={
                "org_id": self.kwargs["org_id"],
                "channel_id": self.kwargs["channel_id"],
            },
        )
