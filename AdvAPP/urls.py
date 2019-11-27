
from django.urls import path
from . import views

app_name = 'AdvAPP'
# another test commit
urlpatterns = [
    path('homepage/', views.home, name='homepage'),
    path('create/<int:story_id>/<int:adv_id>', views.create, name='create'),
    path('create/', views.create_story, name='create_story'),
    path('play/', views.play, name='play'),
    path('start/<int:stories_id>/', views.start, name='start'),
    path('<int:result_text>/', views.playing, name='playing'),
]
