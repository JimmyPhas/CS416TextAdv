from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.http import Http404
try:
    import tweepy
    from tweepy import RateLimitError
except:
    print("tweepy import error")
from config import *
from .models import Stories, AdventureText, ChoiceText
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

def home(request):
    try:
        if request.method == 'POST':
            user = request.POST.get('user')
            return render(request, 'homepage.html', {'tweets': getTweetsUser(user)})
        return render(request, 'homepage.html', {'tweets' : getTweets()})
    except:
        print("error with tweepy  API")
    status = "Problem importing tweepy API"
    return render(request, 'homepage.html', {'tweets': status})

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



