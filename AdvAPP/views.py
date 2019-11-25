from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.http import Http404

from .models import Stories, AdventureText, ChoiceText

# Create your views here.

def home(request):
    template = loader.get_template('homepage.html')
    return HttpResponse(template.render())

def create(request):
    template = loader.get_template('create.html')
    return HttpResponse(template.render())

def play(request):
    stories_list = Stories.objects.all()
    start_list = AdventureText.objects.all().get(adv_text="start").id
    template = loader.get_template('play.html')
    context = {
        'stories_list' : stories_list,
        'start_id': start_list
    }
    return HttpResponse(template.render(context, request))

def start(request, stories_id):
    try:
        adventureText = AdventureText.objects.get(pk=stories_id)
    except AdventureText.DoesNotExist:
        raise Http404("Story does not exist")
    return render(request, 'playing.html', {'adventureText': adventureText})

def playing(request, result_text):
    try:
        adventureText = AdventureText.objects.get(pk=result_text)
    except AdventureText.DoesNotExist:
        raise Http404("Story does not exist")
    return render(request, 'playing.html', {'adventureText': adventureText})


