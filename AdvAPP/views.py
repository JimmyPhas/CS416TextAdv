from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.http import Http404

from .models import Stories, AdventureText, ChoiceText
from .forms import StoryForm, ChoiceForm
# Create your views here.

def home(request):
    template = loader.get_template('homepage.html')
    return HttpResponse(template.render())

def create(request, story_id, adv_id):
    if request.method == 'POST':
        origin_story = Stories.objects.get(pk=story_id)
        branch_story = AdventureText.objects.get(pk=adv_id)
        story_text = request.POST.get("text_input")
        choice_text = request.POST.get("text_result")
        new_text = AdventureText.objects.create(adv_text=story_text, story=origin_story)
        ChoiceText.objects.create(choice_text=choice_text, choice_of=branch_story , result_text=new_text.pk)
        return render(request, 'playing.html', {'adventureText': new_text})
    else:
        return render(request, 'create.html')

def create_story(request):
    if request.method == 'POST':
        story_title = request.POST.get("story_title")
        intro_text = request.POST.get("intro_input")
        next_text = request.POST.get("text_input")
        new_story = Stories.objects.create(story_title=story_title)
        start_text = AdventureText.objects.create(story=new_story, adv_text=intro_text)
        first_text = AdventureText.objects.create(story=new_story, adv_text=next_text)
        ChoiceText.objects.create(choice_text='Start', choice_of=start_text, result_text=first_text.pk)
        return render(request, 'playing.html', {'adventureText': start_text})
    else:
        return render(request, 'storycreate.html')

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


