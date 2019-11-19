from django.db import models

class AdventureText(models.Model):
    adv_text = models.TextField()

class ChoiceText(models.Model):
    choice_text = models.CharField(max_length=300)
    choice_of = models.ForeignKey(AdventureText, related_name='requested_choice', on_delete=models.CASCADE)
    result_text = models.ForeignKey(AdventureText, on_delete=models.CASCADE)

class Stories(models.Model):
    story = models.ForeignKey(AdventureText, on_delete=models.CASCADE)