from django.db import models

# Create your models here.

class CommonInfo(models.Model):
    twitter_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    screen_name = models.CharField(max_length=15)

    class Meta:
        abstract = True

    def __str__(self):
        return self.screen_name

class PostedBy(CommonInfo):
    created_at = models.DateTimeField()

class Mention(CommonInfo):
    in_reply_to_status_id = models.IntegerField()

class Hashtag(models.Model):
    text_lower = models.CharField(max_length=280, primary_key=True)
    count = models.IntegerField(default=0)

    def __str__(self):
        return self.text_lower

class Url(models.Model):
    url = models.CharField(max_length=280)
    expanded_url = models.CharField(max_length=280)
    display_url = models.CharField(max_length=280)

    def __str__(self):
        return self.url

class Tip(models.Model):
    twitter_id = models.IntegerField(primary_key=True)
    timestamp = models.DateTimeField()
    text = models.CharField(max_length=280)
    retweet_count = models.IntegerField(default=0)
    favourite_count = models.IntegerField(default=0)
    posted_by = models.ForeignKey(PostedBy, on_delete=models.CASCADE)
    urls = models.ManyToManyField(Url, null=True, blank=True)
    hashtags = models.ManyToManyField(Hashtag, null=True, blank=True)
    mentions = models.ManyToManyField(Mention, null=True, blank=True)

    class Meta:
        ordering = ["-favourite_count", "-retweet_count"]

    def __str__(self):
        return self.text
