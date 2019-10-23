from django.views.generic.detail import DetailView
from management.mixins import SessionAuthenticationRequiredMixin, SessionOrgContextMixin
from management.models import Organization
from alerts.models import Channel


class ChannelsView(
    SessionAuthenticationRequiredMixin, SessionOrgContextMixin, DetailView
):
    template_name = "management/pages/channels.html"
    model = Organization

class ChannelView(
    SessionAuthenticationRequiredMixin, SessionOrgContextMixin, DetailView
):
    template_name = "management/pages/channel.html"
    model = Channel
