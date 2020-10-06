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

    #path('add_members/<int:group_id>/',views.add_members,name='add_members'),
    #path('upload-csv/<int:group_id>/',views.members_upload,name="members_upload")
]