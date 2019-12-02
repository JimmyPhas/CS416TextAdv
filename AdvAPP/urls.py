
from django.urls import path, include
from . import views

app_name = 'AdvAPP'
# another test commit
urlpatterns = [
    path('homepage/', views.home, name='homepage'),
    path('create/', views.create, name='create'),
    path('play/', views.play, name='play'),
    path('<int:result_text>/', views.playing, name='playing'),
    path('authen/', include('authen.urls'))
]
