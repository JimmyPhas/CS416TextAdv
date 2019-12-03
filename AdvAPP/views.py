from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.http import Http404
import twitter
import tweepy
from tweepy import OAuthHandler, RateLimitError
from config import *
from requests_oauthlib import OAuth1Session


from django.contrib.auth.models import User, auth

from .models import Stories, AdventureText, ChoiceText
from .forms import StoryForm, ChoiceForm
# Create your views here.

def getTweets():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    public_tweets = api.home_timeline(count=10)
    tweets = []
    for tweet in public_tweets:
        status = tweet.text
        tweets.append({'status': status})
    return {'tweets':tweets}

def getTweetsUser(user):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    public_tweets = api.user_timeline(user, count=10)
    tweets = []
    for tweet in public_tweets:
        status = tweet.text
        print(status)
        tweets.append({'status': status})
    return {'tweets':tweets}

def postTweet(up_status):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    api.update_status(up_status)

def home(request):
    try:
        if request.method == 'POST':
            user = request.POST.get('user')
            return render(request, 'homepage.html', {'tweets': getTweetsUser(user)})
        return render(request, 'homepage.html', {'tweets' : getTweets()})
    except tweepy.error.RateLimitError:
        raise RateLimitError("API call limit exceeded")
    return render(request, 'homepage.html')

def create(request):
    return render(request, 'create.html')


def play(request):
    stories_list = Stories.objects.all()
    start_list = ChoiceText.objects.all().filter(choice_text="Start").values_list('choice_of', flat=True)
    template = loader.get_template('play.html')
    my_dict = dict(zip(start_list, stories_list))

    context = {
        'my_dict' : my_dict,
        'stories_list' : stories_list,
        'start_list' : start_list
    }
    return HttpResponse(template.render(context, request))

def playing(request, result_text):
    try:
        adventureText = AdventureText.objects.get(pk=result_text)
    except AdventureText.DoesNotExist:
        raise Http404("Story does not exist")
    return render(request, 'playing.html', {'adventureText': adventureText})



