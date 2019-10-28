from django.db import models
from management.models import Organization
from alerts.models import Channel
from django.core.signing import TimestampSigner
from django.shortcuts import get_object_or_404

# Emails
from django.core.mail import send_mass_mail


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

    unique_together = ["email", "organization"]

    def get_verification_token(self):
        return TimestampSigner().sign(str(self.id))

    @staticmethod
    def activate_verification_token(self, token):
        subscription = get_object_or_404(EmailSubscription, id=TimestampSigner().unsign(token, max_age=24*60*60))
        subscription.verified = True
        subscription.save()


class EmailSubscriptionGroup:
    @staticmethod
    def for_channel(channel):
        return EmailSubscriptionGroup(
            EmailSubscription.objects.filter(channels__contains=channel, verified=True)
        )

    def push(self, alert):
        # TODO: send nice-looking HTML messages, potentially with
        # the news organization's logo
        emails = [
            (
                f"{alert.channel.organization.name}: {alert.channel.name}",
                f"{alert.content}",
                "noreply@outgoing.openalerts.org",
                [subscription.email],
            )
            for subscription in self.subscriptions
        ]
        send_mass_mail(emails)

