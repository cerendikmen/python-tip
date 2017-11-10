from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^search/', views.FullTextSearch.as_view()),
	url(r'^topfavs/', views.MostFavTweets.as_view()),
	url(r'^toprts/', views.MostRetweetedTweets.as_view()),
	url(r'^weekly/', views.WeeklyTweets.as_view()),
	url(r'^tophashtags/', views.TopFiveHashtags.as_view()),
]
