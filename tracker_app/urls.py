from django.urls import path
from tracker_app import views

urlpatterns = [
    path('', views.login, name='login'),
    path('dashboard/', views.userdash, name='userdash'),
    path('dashboard/<int:group_id>/', views.groupdash, name='groupdash'),
]