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

def edit(request, story_title):
    story = Stories.objects.get(story_title=story_title)

    context = {
        'story' : story,
    }
    return render(request, 'edit.html', context)

def create(request,story_id,adv_id):
    if request.method == 'POST':
        origin_story = Stories.objects.get(pk=story_id)
        branch_story = AdventureText.objects.get(pk=adv_id)
        if (request.POST.get("select_input") == "null"):
            story_text = request.POST.get("text_input")
            choice_text = request.POST.get("text_result")
            new_text = AdventureText.objects.create(adv_text=story_text, story=origin_story)
            ChoiceText.objects.create(choice_text=choice_text, choice_of=branch_story, result_text=new_text.pk)
            return render(request, 'playing.html', {'adventureText': new_text})
        else:
            story_text = request.POST.get("select_input")
            choice_text = request.POST.get("text_result")
            new_text = AdventureText.objects.get(pk=story_text)
            ChoiceText.objects.create(choice_text=choice_text, choice_of=branch_story , result_text=new_text.pk)
            return render(request, 'playing.html', {'adventureText': new_text})
    else:
        origin_story = Stories.objects.get(pk=story_id)
        return render(request, 'create.html', { 'story' : origin_story})


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

def playing(request, result_text):
    try:
        adventureText = AdventureText.objects.get(pk=result_text)
    except AdventureText.DoesNotExist:
        raise Http404("Story does not exist")
    return render(request, 'playing.html', {'adventureText': adventureText})

def delete(request, del_type, id):
    if del_type == "story":
        story = Stories.objects.get(pk=id)
        story.delete()
    elif del_type == "adventure":
        adv_text = AdventureText.objects.get(pk=id)
        adv_text.delete()
    elif del_type == "choice":
        choice_text = ChoiceText.objects.get(pk=id)
        choice_text.delete()
    return render(request, 'delete.html', { 'del_type' : del_type })

def update(request, up_type, id):
    if request.method == 'POST':
        if up_type == "story":
            story = Stories.objects.get(pk=id)
            story.story_title = request.POST.get("story_title")
            story.author = request.POST.get("story_author")
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
        return render(request, 'edit.html', context)
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
        return render(request, 'update.html', context)

