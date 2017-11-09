import tweepy

from django.core.management.base import BaseCommand, CommandError
from django.db.models import Max
from python_tip_app.models import *

import os
import datetime
import html

CONSUMER_KEY = os.getenv("TWITTER_CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("TWITTER_CONSUMER_SECRET")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
PYTHON_TIP_ID = os.getenv("TWITTER_PYTHON_TIP_ID")

def local_to_utc(local_dt, utc_offset):
    return local_dt - datetime.timedelta(seconds=utc_offset)

def process_status(status):
    # Creates the author if not created already
    author = status.author
    created_at = local_to_utc(author.created_at, author.utc_offset)
    posted_by, created = PostedBy.objects.get_or_create(twitter_id=author.id, name=author.name, screen_name=author.screen_name, created_at=created_at)

    # Creates tip with the relevant fields provided by status
    text = html.unescape(status.text)
    tip = Tip(twitter_id=status.id, timestamp=status.created_at, text=text,
            retweet_count=status.retweet_count, favorite_count=status.favorite_count,
            posted_by=posted_by)
    tip.save()
    # Gets urls, hashtags and mentions if exist in the tweet aka status
    urls = status.entities['urls']
    hashtags = status.entities['hashtags']
    mentions = status.entities['user_mentions']

    # Urls in the tweet aka status created and added to tweet model
    if urls:
        for u in urls:
            url = tip.urls.create(url=u.get('url'), expanded_url=u.get('expanded_url'), display_url=u.get('display_url'))
    # Hashtags in the tweet aka status created and added to tweet model
    if hashtags:
        for h in hashtags:
            try:
                if 'text' in h:
                    hashtag, created = Hashtag.objects.get_or_create(text_lower=h['text'].lower())
                if not created:
                    hashtag.count += 1
                    hashtag.save()
                    tip.hashtags.add(hashtag)
            except  Hashtag.MultipleObjectsReturned:
                print("There are multiple hashtags with the same text.")

    # Mentions in the tweet aka status created and added to tweet model
    if mentions:
        for m in mentions:
            mention = tip.mentions.create(twitter_id=m.get('id'), name=m.get('name'), screen_name=m.get('screen_name'), in_reply_to_status_id=status.in_reply_to_status_id)


class Command(BaseCommand):
    help = 'Syncs the published tips to a DB from python_tip Twitter account using a wrapper called Tweepy.'

    def handle(self, *args, **options):
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

        api = tweepy.API(auth)
        dic =   {
                    'id' : PYTHON_TIP_ID,
                    'exclude_replies' : True,
                    'include_rts' : False
                }
        result = Tip.objects.aggregate(max_id=Max('twitter_id'))
        if result['max_id']:
            print("result max id var: ", result['max_id'])
            dic['since_id'] = result['max_id']
        cursor = tweepy.Cursor(api.user_timeline, **dic)
        for status in cursor.items():
            process_status(status)
