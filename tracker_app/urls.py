from django.urls import path
from tracker_app import views

app_name = 'tracker_app'
urlpatterns = [
    path('', views.index, name='index'),

    path('dashboard/', views.userdash, name='userdash'),
    path('creategroup/',views.creategroup,name='creategroup'),
    path('addmember/<int:group_id>/',views.addmember,name='addmember'),
    path('dashboard/<int:group_id>/', views.groupdash, name='groupdash'),
    path('dashboard/<int:group_id>/<int:mem_id>/', views.groupdash, name='groupmemdash'),

    path('dashboard/<int:group_id>/reportissue/', views.reportissue, name='reportissue'),
    path('dashboard/<int:group_id>/removeissue/', views.removeissue, name='removeissue'),
    path('displayissues/<int:group_id>/', views.displayissues, name='displayissues'),
]