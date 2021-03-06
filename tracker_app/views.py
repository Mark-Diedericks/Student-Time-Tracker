from django.urls import reverse
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required

from tracker_app import forms
from tracker_app import models
from tracker_app import utils

from tracker_app.indv_views import userdashview
from tracker_app.indv_views import groupdashview
from tracker_app.indv_views import creategroupview
from tracker_app.indv_views import addmemberview
from tracker_app.indv_views import manageroles
from tracker_app.indv_views import issuemanager

import csv, io
from django.contrib import messages



# Create your views here.
def index(request):
    # https://docs.djangoproject.com/en/3.1/topics/auth/default/#auth-web-requests

    if (request.user is not None) and (request.user.is_authenticated):
        return redirect('/dashboard/')      # We have a user, goto dashboard
    else:
        return redirect('/login/')          # We don't have a user, goto login


##### USER DASH ######
@login_required
def userdash(request):
    return userdashview.userdash(request)


##### GROUP DASH ######
@login_required
def groupdash(request, group_id, mem_id = -1):
    return groupdashview.groupdash(request, group_id, mem_id)
    

##### ADD ROLE ######
@login_required
def addrole(request, group_id):
    return manageroles.addrole(request, group_id)
    
    
##### SET ROLE ######
@login_required
def setroles(request, group_id, mem_id):
    return manageroles.setroles(request, group_id, mem_id)


##### GROUP CREATE ######
@login_required
def creategroup(request):
    return creategroupview.creategroup(request)


##### ADD MEMBER ######
@login_required
def addmember(request,group_id):
    return addmemberview.addmember(request,group_id)


##### ADD ISSUE ######
@login_required
def reportissue(request, group_id):
    return issuemanager.reportissue(request, group_id)


##### REMOVE ISSUE ######
@login_required
def removeissue(request, group_id):
    return issuemanager.removeissue(request, group_id)


##### DISPLAY ISSUES ######
@login_required
def displayissues(request, group_id):
    return issuemanager.display_issues(request, group_id)