from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.

def home(request):
    template = loader.get_template('homepage.html')
    return HttpResponse(template.render())

def create(request):
    template = loader.get_template('create.html')
    return HttpResponse(template.render())

def play(request):
    template = loader.get_template('play.html')
    return HttpResponse(template.render())