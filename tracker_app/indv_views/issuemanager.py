from tracker_app.models import SubmittedPeriod
from django.urls import reverse
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404

from tracker_app import forms
from tracker_app import models
from tracker_app import utils

import csv, io
from django.contrib import messages

from datetime import datetime




#add function for reportissue
def reportissue(request, group_id):  

    # Attempt to get the group, group's members and group's tasks
    try:
        g = models.Group.objects.get(pk = group_id)
        mem = models.GroupMember.objects.filter(group = g).get(person = request.user)
    except:                                     # Group doesn't exist, go back to userdash 
        return JsonResponse({'status': 'bad'})

    # Attempt to create the issue and save it to the database
    try:        
        submission_date = datetime.combine(datetime.today(), datetime.min.time())   
        name = request.POST['title']
        desc = request.POST['description']
        # Create a report issue and save it
        issue = models.ReportIssue(group = g, groupMember = mem, title = name, description = desc, dateSubmitted = submission_date)
        issue.save()
    except:
        print("Failed to get POST component", request.POST['title'], request.POST['description']) 
        return JsonResponse({'status': 'bad'})

    return JsonResponse({'status': 'ok'})


def display_issues(request, group_id):

    # Attempt to get the group, group's members and group's tasks
    try:
        g = models.Group.objects.get(pk = group_id)
        mem = models.GroupMember.objects.filter(group = g).get(person = request.user)
        mems = list(models.GroupMember.objects.filter(group = g))
    except:                                     # Group doesn't exist, go back to userdash 
        print("Group does not exist ", group_id)
        return redirect('/dashboard/')
    
    # Get user member and check if the user is an 'owner' of the group
    user_mem = utils.get_user_member(mems, request.user)
    is_owner = utils.is_owner(user_mem)

    issues = []
    try:
        # Get the all issues of the group
        issues = list(models.ReportIssue.objects.filter(group = g))
    except:                                     # Member does not exist, continue without any selection
        print("No issues reported ")
    
    return render(request, 'displayissues.html', {'group': g, 'issues': issues, 'active_member': mem, 'is_owner': is_owner, 'title': g.groupName})