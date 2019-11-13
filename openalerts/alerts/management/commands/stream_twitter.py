from django.core.management.base import BaseCommand, CommandError
from alerts.models import Alert, Source
from django.conf import settings
import tweepy

class Command(BaseCommand):
    help = 'Streams new alerts from Twitter'

    def handle(self, *args, **options):
        self.stdout.write("Launching streamer...")
        sources = Source.objects.filter(source="TWITTER")

        auth = tweepy.OAuthHandler(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET)
        auth.set_access_token(settings.TWITTER_ACCESS_TOKEN, settings.TWITTER_ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth)

        for source in sources:
            if source.identifier == None:
                self.stdout.write(f"Populating ID for new source {source.human_readable_identifier}...")
                real_id = api.get_user(source.human_readable_identifier).id_str
                source.identifier = real_id
                source.save()

        ids = [source.identifier for source in sources]

        cmd = self

        class OpenAlertsStreamListener(tweepy.StreamListener):
            def on_status(self, status):
                # Find linked source
                source = Source.objects.filter(source="TWITTER", identifier=status.user.id_str)
                if source.exists():
                    source = source.first()
                else:
                    return

                # Get core data
                text = status.text
                if hasattr(status, "extended_tweet"):
                    text = status.extended_tweet.full_text
                url = ""
                if hasattr(status, "urls") and len(status.urls) > 0:
                    url = status.urls[0].expanded_url                

                Alert.objects.create(channel=source.channel, content=text, url=url, source=source, source_identifier=status.id_str)

                cmd.stdout.write(f"Published new alert from {source.human_readable_identifier} in channel {source.channel}: '{text}'")

        auth = tweepy.OAuthHandler(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET)
        auth.set_access_token(settings.TWITTER_ACCESS_TOKEN, settings.TWITTER_ACCESS_TOKEN_SECRET)
        
        stream = tweepy.Stream(auth, OpenAlertsStreamListener(), async=False)

        user = api.me()

        self.stdout.write(self.style.SUCCESS(f"Opening stream monitoring {sources.count()} sources on Twitter as @{user.screen_name}..."))
        stream.filter(follow=ids)