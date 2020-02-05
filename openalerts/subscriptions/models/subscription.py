from django.db import models, transaction
from django.conf import settings
from management.models import Organization
from alerts.models import Channel, AlertStats
from django.core.signing import TimestampSigner
from django.shortcuts import get_object_or_404, reverse
from django.template.loader import render_to_string
from webpush.models import PushInformation, Group
from webpush.utils import send_notification_to_group
import json

# Emails
from django.core.mail import send_mass_mail, send_mail


# SUBSCRIPTION GROUPS
# -------------------

# A SubscriptionGroup is a collection of subscriptions that are
# grouped for (the opportunity of) greater efficiency when
# doing a 'multicast send' (i.e. broadcast). After all, it's
# far more efficient to send one message to many emails, for example,
# than to send the message one email at a time.
class SubscriptionGroup:
    def __init__(self, subscriptions):
        self.subscriptions = subscriptions

    # Get all the subscribers to a particular channel and
    # assemble them into a new SubscriptionGroup that
    # can be used for sending.
    @staticmethod
    def for_channel(channel):
        raise NotImplementedError

    # Push the given alert to every subscription in the
    # SubscriptionGroup. Naive implementations will
    # send the message to each subscription indiv-
    # idually, but better ones will make use of
    # multicast systems (like Django's multi-email
    # send functionality).
    def push(self, alert):
        raise NotImplemented


# EMAIL SUBSCRIPTIONS
# -------------------


class EmailSubscription(models.Model):
    email = models.EmailField()
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    channels = models.ManyToManyField(Channel)
    verified = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    unique_together = ["email", "organization"]

    def get_verification_token(self):
        return TimestampSigner().sign(str(self.id))

    @staticmethod
    def activate_verification_token(token):
        subscription = get_object_or_404(
            EmailSubscription, id=TimestampSigner().unsign(token, max_age=24 * 60 * 60)
        )
        subscription.verified = True
        subscription.save()
        return subscription

    def get_access_token(self):
        return TimestampSigner().sign(str(self.id))

    @staticmethod
    def for_access_token(token):
        return get_object_or_404(
            EmailSubscription,
            id=TimestampSigner().unsign(token, max_age=30 * 24 * 60 * 60),
        )

    def send_opt_in(self):
        link = "/TODO"
        send_mail(
            "Confirm email sign-up",
            render_to_string(
                "subscriptions/email/opt-in.txt",
                context={
                    "link": link,
                    "organization": self.organization,
                    "subscription": self,
                    "link_prefix": settings.PROTOCOL_AND_HOST,
                },
            ),
            f"{self.organization.name} <{settings.EMAIL_FROM}>",
            [self.email],
        )


class EmailSubscriptionGroup(SubscriptionGroup):
    @staticmethod
    def for_channel(channel):
        return EmailSubscriptionGroup(
            EmailSubscription.objects.filter(channels__in=[channel], verified=True)
        )

    def push(self, alert):
        # TODO: send nice-looking HTML messages, potentially with
        # the news organization's logo
        emails = [
            (  # TODO: design nice message template
                f"{alert.channel.organization.name}: {alert.channel.name}",
                render_to_string(
                    "subscriptions/email/alert.txt",
                    context={
                        "alert": alert,
                        "alert_url": alert.get_public_url("em"),
                        "organization": subscription.organization,
                        "subscription": subscription,
                        "link_prefix": settings.PROTOCOL_AND_HOST,
                    },
                ),
                f"{alert.channel.organization.name} <{settings.EMAIL_FROM}>",
                [subscription.email],
            )
            for subscription in self.subscriptions
        ]
        send_mass_mail(emails)

        with transaction.atomic():
            stats = AlertStats.for_alert_locking(alert)
            stats.email_sends += len(self.subscriptions)
            stats.save()


# WEBPUSH SUBSCRIPTIONS
# ---------------------


class WebpushSubscription(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    subscription = models.ForeignKey(PushInformation, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)


class WebpushSubscriptionGroup(SubscriptionGroup):
    def __init__(self, group):
        self.group = group
        super(WebpushSubscriptionGroup, self).__init__(None)

    @staticmethod
    def for_channel(channel):
        group = Group.objects.get(name=str(channel.organization.id))
        return WebpushSubscriptionGroup(group)

    def push(self, alert):
        send_notification_to_group(
            self.group.name,
            payload=json.dumps(
                {
                    "head": f"{alert.channel.name} / {alert.channel.organization.name}",  # TODO: make configurable
                    "body": alert.content,
                    "url": settings.PROTOCOL_AND_HOST + alert.get_public_url("wp"),
                }
            ),
            ttl=1000,
        )
        with transaction.atomic():
            stats = AlertStats.for_alert_locking(alert)
            stats.webpush_sends += WebpushSubscription.objects.filter(
                organization=alert.channel.organization
            ).count()
            stats.save()
