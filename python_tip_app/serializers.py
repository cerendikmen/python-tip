from rest_framework import serializers
from .models import Tip, Hashtag

class TipSerializer(serializers.ModelSerializer):
	class Meta:
		model = Tip
		fields = ('text', 'timestamp', 'retweet_count', 'favorite_count')

class HashtagSerializer(serializers.ModelSerializer):
	class Meta:
		model = Hashtag
		fields = '__all__'
