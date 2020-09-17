from django.urls import path
from tracker_app import views

app_name = 'tracker_app'
urlpatterns = [
    path('', views.index, name='index'),
    
    # path('login/', views.login, name='login'),
    # path('signup/', views.signUp, name='signup'),

    path('dashboard/', views.userdash, name='userdash'),
    path('creategroup/',views.CreateGroup,name='CreateGroup'),
    
    path('dashboard/<int:group_id>/', views.groupdash, name='groupdash'),
    path('dashboard/<int:group_id>/<int:mem_id>/', views.groupdash, name='groupmemdash'),
    path('dashboard/<int:group_id>/<int:mem_id>/logtime', views.logtime, name='logtime'),
]