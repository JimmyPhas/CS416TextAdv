
from django.urls import path
from . import views

app_name = 'authen'
# another test commit
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout')
]