
from django.urls import path
from . import views


app_name = 'authen'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('stories/', views.user_stories, name='user_stories'),
    path('create/', views.userCreate, name='user_create'),
    path('create/<int:story_id>/<int:text_id>', views.user_add, name='user_add'),
    path('edit/<str:story_title>/', views.user_edit, name='user_edit'),
    path('update/<str:up_type>/<int:id>', views.user_update, name='user_update'),
    path('delete/<str:del_type>/<int:id>', views.user_delete, name='user_delete'),
    path('homepage/', views.homepage, name='auth_homepage'),
    path('play/', views.play, name="auth_play"),
    path('<int:result_text>/', views.playing, name='playing'),
    path('publish/<int:story_id>/', views.publish, name="publish")
]