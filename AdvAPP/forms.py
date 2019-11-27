from django import forms
from django.forms import ModelForm
from .models import AdventureText, ChoiceText


class StoryForm(ModelForm):
    class Meta:
        model = AdventureText
        fields = ['adv_text']

class ChoiceForm(ModelForm):
    class Meta:
        model = ChoiceText
        fields = ['choice_text', 'choice_of', 'result_text']