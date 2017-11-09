from rest_framework import serializers
from .models import Tip

class TipSerializer(serializers.ModelSerializer):
	class Meta:
		model = Tip
		fields = ('text', 'retweet_count', 'favorite_count')
