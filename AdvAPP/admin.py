from django.contrib import admin
from .models import Stories, AdventureText, ChoiceText
# Register your models here.
admin.site.register(Stories),
admin.site.register(AdventureText),
admin.site.register(ChoiceText),