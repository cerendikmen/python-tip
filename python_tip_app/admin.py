from django.contrib import admin
from .models import *

# Register your models here.
class PostedByAdmin(admin.ModelAdmin):
    list_display = ('twitter_id', 'screen_name')

class MentionAdmin(admin.ModelAdmin):
    list_display = ('twitter_id', 'screen_name', 'in_reply_to_status_id')

class HashtagAdmin(admin.ModelAdmin):
    list_display = ('text_lower', 'count')

class UrlAdmin(admin.ModelAdmin):
    exclude = ('display_url',)
    list_display = ('url', 'expanded_url')

class TipAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'text', 'retweet_count', 'favorite_count',
                'posted_by', 'get_tip_urls', 'get_hashtags', 'get_mentions')
    date_hierarchy = 'timestamp'
    list_filter = ('timestamp', 'hashtags')
    search_fields = ['^=hashtags__text_lower']
    filter_horizontal = ('hashtags', 'urls', 'mentions')

    def get_tip_urls(self, obj):
        return ','.join([u.display_url for u in obj.urls.all()])
    get_tip_urls.short_descripton = 'urls'

    def get_hashtags(self, obj):
        return ','.join([h.text_lower for h in obj.hashtags.all()])
    get_hashtags.short_descripton = 'hashtags'
    
    def get_mentions(self, obj):
        return ','.join([m.screen_name for m in obj.mentions.all()])
    get_mentions.short_descripton = 'mentions'

admin.site.register(PostedBy, PostedByAdmin)
admin.site.register(Mention, MentionAdmin)
admin.site.register(Hashtag, HashtagAdmin)
admin.site.register(Url, UrlAdmin)
admin.site.register(Tip, TipAdmin)
