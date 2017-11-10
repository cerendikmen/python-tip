from django.db import models
from django.contrib.postgres.search import SearchVector, SearchVectorField
from django.contrib.postgres.aggregates import StringAgg
from django.contrib.postgres.indexes import GinIndex

# Create your models here.
class TipManager(models.Manager):
    def with_documents(self):
        vector = (SearchVector('text', weight='A') +
                    SearchVector(StringAgg('hashtags__text_lower', delimiter=' '), weight='A') +
                    SearchVector(StringAgg('urls__expanded_url', delimiter=' '), weight='B'))
        return self.get_queryset().annotate(document=vector)
    
class TopFiveFavTipManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by('-favorite_count')[:5]

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
    search_vector = SearchVectorField(null=True)
    objects = TipManager()
    top5_fav_objects = TopFiveFavTipManager()

    class Meta:
        ordering = ["-favorite_count", "-retweet_count"]
        indexes = [GinIndex(fields=['search_vector'])]

    def __str__(self):
        return self.text

    def save(self, *args, **kwargs):
        super().save( *args, *kwargs)
        if 'update_fields' not in kwargs or 'search_vector' not in kwargs['update_fields']:
            instance = self._meta.default_manager.with_documents().filter(pk=self.pk)
            instance.update(search_vector=instance[0].document)
