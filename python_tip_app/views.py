from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from django.db.models import F
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.contrib.postgres.aggregates import StringAgg

import functools
import operator

from .models import *
from .serializers import TipSerializer, HashtagSerializer

# Create your views here.

class FullTextSearch(APIView):
    def post(self, request, format=None):
        search_str = request.data.get('search', '')
        query = [SearchQuery(term) for term in search_str.split()]
        query = functools.reduce( operator.or_, query)
        queryset =  (Tip.objects.annotate(rank=SearchRank(F('search_vector'), query))
                    .filter(search_vector=query).order_by('-rank'))
        tweets = TipSerializer(queryset, many=True)
        return Response(tweets.data)

class MostFavTweets(ListAPIView):
    serializer_class = TipSerializer
    queryset =  Tip.top_five_fav_objects.all()

class MostRetweetedTweets(ListAPIView):
    serializer_class = TipSerializer
    queryset =  Tip.top_five_retweeted_objects.all()

class WeeklyTweets(ListAPIView):
    serializer_class = TipSerializer
    queryset =  Tip.weekly_objects.all()

class TopFiveHashtags(ListAPIView):
    serializer_class = HashtagSerializer
    queryset = Hashtag.top_five_objects.all()
