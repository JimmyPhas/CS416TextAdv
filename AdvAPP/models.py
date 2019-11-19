from django.db import models

class AdventureText(models.Model):
    adv_text = models.CharField(max_length=500)

class ChoiceText(models.Model):
    choice_text = models.CharField(max_length=300)
    choice_of = models.ForeignKey(AdventureText, related_name='requested_choice', on_delete=models.CASCADE)
    result_text = models.ForeignKey(AdventureText, on_delete=models.CASCADE)