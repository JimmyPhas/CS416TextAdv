
from django.urls import path
from . import views

# another test commit
urlpatterns = [
    path('homepage/', views.home, name='homepage'),
    path('create/', views.create, name='create'),
    path('play/', views.play, name='play'),
]
