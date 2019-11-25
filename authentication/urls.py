
from django.urls import path
from . import views

app_name = 'AdvAPP'
# another test commit
urlpatterns = [
    path('homepage/', views.home, name='homepage'),
    path('create/', views.create, name='create'),
    path('play/', views.play, name='play'),
    path('start/<int:stories_id>/', views.start, name='start'),
    path('<int:result_text>/', views.playing, name='playing'),
]