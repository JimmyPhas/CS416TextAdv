from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.http import Http404
from django.contrib.auth.models import User, auth

from .models import Stories, AdventureText, ChoiceText
from .forms import StoryForm, ChoiceForm
# Create your views here.

def home(request):
    template = loader.get_template('homepage.html')
    return HttpResponse(template.render())

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



