from django.urls import path
from tracker_app import views

app_name = 'tracker_app'
urlpatterns = [
    path('', views.index, name='index'),

    path('login/', views.login, name='login'), # Pretty sure django already has a login page built-in so this is redundant...
    path('dashboard/', views.userdash, name='userdash'),
    path('dashboard/<int:group_id>/', views.groupdash, name='groupdash'),
]