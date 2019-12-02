from django.db import models
from django.contrib.auth.models import User, AnonymousUser

class Stories(models.Model):
    story_title = models.CharField(max_length=100)
    author = models.CharField(max_length=100, default="anonymous")
    published = models.BooleanField(default=False)
    def __str__(self):
        return self.story_title

class AdventureText(models.Model):
    story = models.ForeignKey(Stories, default="", on_delete=models.CASCADE)
    adv_text = models.TextField()
    def __str__(self):
        return self.adv_text

class ChoiceText(models.Model):
    choice_text = models.CharField(max_length=300)
    choice_of = models.ForeignKey(AdventureText, on_delete=models.CASCADE)
    result_text = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text
