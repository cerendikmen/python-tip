from django.db import models

# Create your models here.

class CommonInfo(models.Model):
    name = models.CharField(max_length=20)
    screen_name = models.CharField(max_length=15)

    class Meta:
        abstract = True

    def __str__(self):
        return self.screen_name

class PostedBy(CommonInfo):
    twitter_id = models.BigIntegerField(unique=True)
    created_at = models.DateTimeField()

class Mention(CommonInfo):
    twitter_id = models.BigIntegerField()
    in_reply_to_status_id = models.BigIntegerField(null=True)

class Hashtag(models.Model):
    text_lower = models.CharField(max_length=280, primary_key=True)
    count = models.IntegerField(default=0)

    class Meta:
        ordering = ["-count"]

    def __str__(self):
        return self.text_lower

class Url(models.Model):
    url = models.CharField(max_length=280)
    expanded_url = models.CharField(max_length=280)
    display_url = models.CharField(max_length=280)

    def __str__(self):
        return self.display_url

class Tip(models.Model):
    twitter_id = models.BigIntegerField(unique=True)
    timestamp = models.DateTimeField()
    text = models.CharField(max_length=280)
    retweet_count = models.IntegerField(default=0)
    favorite_count = models.IntegerField(default=0)
    posted_by = models.ForeignKey(PostedBy, on_delete=models.CASCADE)
    urls = models.ManyToManyField(Url, null=True, blank=True)
    hashtags = models.ManyToManyField(Hashtag, null=True, blank=True)
    mentions = models.ManyToManyField(Mention, null=True, blank=True)

    class Meta:
        ordering = ["-favorite_count", "-retweet_count"]

    def __str__(self):
        return self.text
