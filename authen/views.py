from django.contrib import messages
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User, auth
from django.template import loader
from AdvAPP.models import Stories, AdventureText, ChoiceText

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
                return redirect('register')
            elif User.objects.filter(email = e_mail).exists():
                print("Email is taken, must be unique")
                messages.info(request, 'Email is taken, must be unique')
                return redirect('register')
            else:
                User.objects.create_user(first_name=firstname, last_name=lastname, email=e_mail, username=user, password=password1)
                print("A user has been created!")
        else:
            print("Passwords do not match!")
            messages.info(request, 'Passwords do not match!')
            return redirect('register')

        return redirect('AdvAPP:homepage')

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
            return redirect('login')
    else:
        return render(request, 'authen/login.html')

def logout(request):
    auth.logout(request)
    return redirect('AdvAPP:homepage')

def user_stories(request):
    if request.user.is_authenticated:
        username = request.user.get_username()
        stories_list = Stories.objects.all().filter(author=username)
        start_list = ChoiceText.objects.all().filter(choice_text="Start").values_list('choice_of', flat=True)
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
            return render(request, 'playing.html', {'adventureText': start_text})
    else:
        return render(request, 'authen/usercreate.html')

def user_edit(request, story_title):
    story = Stories.objects.get(story_title=story_title)

    context = {
        'story' : story,
    }
    return render(request, 'edit.html', context)

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
    return render(request, 'delete.html', { 'del_type' : del_type })

def user_update(request, up_type, id):
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

def homepage(request):
    return render('homepage.html',request)