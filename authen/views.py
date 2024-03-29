from django.contrib import messages
from django.http import Http404
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User, auth
from django.template import loader

from AdvAPP.models import Stories, AdventureText, ChoiceText

try:
    import tweepy
    from tweepy import RateLimitError
except:
    print("tweepy import error")
from config import *
from . import views


def register(request):
    if request.method == 'POST':
        firstname = request.POST['first_name']
        lastname = request.POST['last_name']
        e_mail = request.POST['email']
        user = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username = user).exists():
                print("Username is taken, must be unique")
                messages.info(request, 'Username is taken, must be unique')
                return redirect('AdvAPP:authen:register')
            elif User.objects.filter(email = e_mail).exists():
                print("Email is taken, must be unique")
                messages.info(request, 'Email is taken, must be unique')
                return redirect('AdvAPP:authen:register')
            else:
                User.objects.create_user(first_name=firstname, last_name=lastname, email=e_mail, username=user, password=password1)
                print("A user has been created!")
        else:
            print("Passwords do not match!")
            messages.info(request, 'Passwords do not match!')
            return redirect('AdvAPP:authen:register')

        return redirect('AdvAPP:authen:auth_homepage')

    else:
        return render(request, 'authen/register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('AdvAPP:authen:user_stories')
        else:
            messages.info(request, 'Invalid credentials')
            return redirect('AdvAPP:authen:login')
    else:
        return render(request, 'authen/login.html')

def logout(request):
    auth.logout(request)
    return redirect('AdvAPP:homepage')

def user_stories(request):
    if request.user.is_authenticated:
        username = request.user.get_username()
        stories_list = Stories.objects.all().filter(author=username)
        start_list = ChoiceText.objects.all().filter(choice_text="Start", choice_of__story__author=username).values_list('choice_of', flat=True)
        #template = loader.get_template('authen/userstories.html')
        my_dict = dict(zip(start_list, stories_list))

        context = {
            'my_dict': my_dict,
            'stories_list': stories_list,
            'start_list': start_list
        }
        return render(request, 'authen/userstories.html', context)
    else:
        return redirect('AdvAPP:homepage')

def userCreate(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            user = request.user.get_username()
            story_title = request.POST.get("story_title")
            intro_text = request.POST.get("intro_input")
            next_text = request.POST.get("text_input")
            new_story = Stories.objects.create(story_title=story_title, author=user)
            start_text = AdventureText.objects.create(story=new_story, adv_text=intro_text)
            first_text = AdventureText.objects.create(story=new_story, adv_text=next_text)
            ChoiceText.objects.create(choice_text='Start', choice_of=start_text, result_text=first_text.pk)
            return redirect('AdvAPP:authen:playing', start_text.id)
    else:
        return render(request, 'authen/usercreate.html')

def user_edit(request, story_title):
    story = Stories.objects.get(story_title=story_title)

    context = {
        'story' : story,
    }
    return render(request, 'authen/useredit.html', context)

def user_delete(request, del_type, id):
    if del_type == "story":
        story = Stories.objects.get(pk=id)
        story.delete()
    elif del_type == "adventure":
        adv_text = AdventureText.objects.get(pk=id)
        adv_text.delete()
    elif del_type == "choice":
        choice_text = ChoiceText.objects.get(pk=id)
        choice_text.delete()
    return render(request, 'authen/userdelete.html', { 'del_type' : del_type })

def user_update(request, up_type, id):
    if request.method == 'POST':
        if up_type == "story":
            story = Stories.objects.get(pk=id)
            story.story_title = request.POST.get("story_title")
            story.save()
            context = {
                'story': story,
            }
        elif up_type == "adventure":
            adv_text = AdventureText.objects.get(pk=id)
            adv_text.adv_text = request.POST.get("text_input")
            adv_text.save()
            context = {
                'story': adv_text.story,
            }
        elif up_type == "choice":
            choice_text = ChoiceText.objects.get(pk=id)
            choice_text.choice_text = request.POST.get("text_result")
            choice_text.save()
            context = {
                'story': choice_text.choice_of.story,
            }
        return render(request, 'authen/useredit.html', context)
    else:
        if up_type == "story":
            story = Stories.objects.get(pk=id)
            context = {
                'del_type': up_type,
                'story' : story
            }
        elif up_type == "adventure":
            adv_text = AdventureText.objects.get(pk=id)
            context = {
                'del_type': up_type,
                'adv_text' : adv_text
            }
        elif up_type == "choice":
            choice_text = ChoiceText.objects.get(pk=id)
            context = {
                'del_type': up_type,
                'choice_text' : choice_text
            }
        return render(request, 'authen/userupdate.html', context)

def homepage(request):
    try:
        if request.method == 'POST':
            user = request.POST.get('user')
            return render(request, 'homepage.html', {'tweets': getTweetsUser(user)})
        return render(request, 'homepage.html', {'tweets' : getTweets()})
    except:
        print("error with tweepy  API")
    status = "Problem importing tweepy API"
    return render(request, 'homepage.html', {'tweets': status})

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

def user_add(request, story_id, text_id):
    if request.method == 'POST':
        story = Stories.objects.get(pk=story_id)
        prev_text = AdventureText.objects.get(pk=text_id)
        if (request.POST.get("select_input") == "null"):
            new_text = request.POST.get("text_input")
            new_choice = request.POST.get("text_result")
            adventure_text = AdventureText.objects.create(story=story, adv_text=new_text)
            ChoiceText.objects.create(choice_text=new_choice, choice_of=prev_text, result_text=adventure_text.id)
            return redirect('AdvAPP:authen:playing', adventure_text.id)
        else:
            new_text = request.POST.get("select_input")
            new_choice = request.POST.get("text_result")
            adventure_text = AdventureText.objects.get(pk=new_text)
            ChoiceText.objects.create(choice_text=new_choice, choice_of=prev_text, result_text=adventure_text.id)
            return redirect('AdvAPP:authen:playing', adventure_text.id)
    else:
        origin_story = Stories.objects.get(pk=story_id)
        title = origin_story.story_title
        return render(request, 'authen/useradd.html',{'story_id':story_id, 'text_id':text_id, 'story' : origin_story, 'title': title})

def publish(request, story_id):
    if request.method == 'POST':
        story = Stories.objects.get(pk=story_id)
        story.published = True
        story.save()
        start_id = str(ChoiceText.objects.get(choice_text="Start", choice_of__story=story_id).choice_of.id)
        tweet_text = story.author + " just published a new story on the site called " + story.story_title + " at JimmyPhas.pythonanywhere.com/AdvAPP/" + start_id
        postTweet(tweet_text)
        return redirect('AdvAPP:authen:auth_play')
    else:
        return render(request, 'authen/publish.html', {'story_id':story_id})

def postTweet(up_status):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    api.update_status(up_status)

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