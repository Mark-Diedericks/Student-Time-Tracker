from django.urls import path
from tracker_app import views

app_name = 'tracker_app'
urlpatterns = [
    path('', views.index, name='index'),
    
    path('signin/', views.login, name='signin'),
    path('signup/', views.signUp, name='signUp'),

    path('dashboard/', views.userdash, name='userdash'),
    path('dashboard/<int:group_id>/', views.groupdash, name='groupdash'),
]