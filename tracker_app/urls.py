from django.urls import path
from tracker_app import views

urlpatterns = [
    path('', views.login, name='Login'),
    path('signUp/', views.signUp, name='signUp'),
]