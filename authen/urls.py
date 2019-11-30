
from django.urls import path
from . import views

app_name = 'authen'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('stories/', views.user_stories, name='user_stories'),
    path('new_story', views.userCreate, name='user_create')
]