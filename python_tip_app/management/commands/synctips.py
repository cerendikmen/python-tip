import tweepy

from django.core.management.base import BaseCommand, CommandError
from python_tip_app.models import *

import os

CONSUMER_KEY = os.getenv("TWITTER_CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("TWITTER_CONSUMER_SECRET")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

class Command(BaseCommand):
    help = 'Syncs the published tips to a DB from python_tip Twitter account using a wrapper called Tweepy.'

    def handle(self, *args, **options):
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

        api = tweepy.API(auth)
