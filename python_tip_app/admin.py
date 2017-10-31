from django.contrib import admin
from .models import *

# Register your models here.

class UrlAdmin(admin.ModelAdmin):
    exclude = ('display_url',)

class TipAdmin(admin.ModelAdmin):
    date_hierarchy = 'timestamp'
    list_filter = ('timestamp', 'hashtags')
    search_fields = ['^=hashtags__text_lower']
    filter_horizontal = ('hashtags', 'urls', 'mentions')

admin.site.register(PostedBy)
admin.site.register(Mention)
admin.site.register(Hashtag)
admin.site.register(Url, UrlAdmin)
admin.site.register(Tip, TipAdmin)
