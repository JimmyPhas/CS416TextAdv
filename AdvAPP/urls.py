
from django.urls import path, include
from . import views

app_name = 'AdvAPP'
# another test commit
urlpatterns = [
    path('homepage/', views.home, name='homepage'),
    path('create/<int:story_id>/<int:adv_id>', views.create, name='create'),
    path('create/', views.create_story, name='create_story'),
    path('play/', views.play, name='play'),
    path('<int:result_text>/', views.playing, name='playing'),
    path('edit/<str:story_title>/', views.edit, name='edit'),
    path('delete/<str:del_type>/<int:id>', views.delete, name='delete'),
    path('update/<str:up_type>/<int:id>', views.update, name='update'),
    path('authen/', include('authen.urls'))
]
