from django.urls import reverse
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import redirect, render, get_object_or_404

from tracker_app import forms
from tracker_app import models
from tracker_app import utils

import csv, io
from django.contrib import messages



##### GROUP DASH ######
def groupdash(request, group_id, mem_id = -1):

    staff = utils.is_staff(request.user)

    mem = None
    user_mem = None
    members = []


    # Attempt to get the group, group's members and group's tasks
    try:
        g = models.Group.objects.get(pk = group_id)
        mems = list(models.GroupMember.objects.filter(group = g))
        tasks = list(models.TaskCategory.objects.filter(group = g))
    except:                                     # Group doesn't exist, go back to userdash 
        print("Group does not exist ", group_id)
        return redirect('/dashboard/')


    # Get user member and check if the user is an 'owner' of the group
    user_mem = utils.get_user_member(mems, request.user)
    owner = utils.is_owner(user_mem)

    # TODO, ensure user can view stuff.
    if (user_mem is not None) and (mem_id != user_mem.id) and (not owner):
        return HttpResponseRedirect(reverse("tracker_app:groupmemdash", args=(group_id, user_mem.id)))


    try:                                        
        # Get the GroupMember of the select user
        mem = models.GroupMember.objects.filter(group = g).get(pk = mem_id)
    except:                                     # Member does not exist, continue without any selection
        print("Member does not exist ", mem_id)
        #return HttpResponseRedirect(reverse("tracker_app:groupdash", args=(group_id)))
    
    members = utils.get_member_times(g, mems, tasks, user_mem)

    # If there is POST data, it is a logtime request. Handle logging.
    if (request.method == "POST") and (g is not None) and (mem is not None):
        return logtime(request, g, mem)
    
    return render(request, 'groupdash.html', {'group': g, 'members': members, 'tasks': tasks, 'active_member': mem, 'is_staff': staff, 'is_owner': owner, 'title': g.groupName})


def logtime(request, group, member):   
    # If there is no POST data, show the normal groupdash
    if request.method != "POST":
        return groupdash(request, group.id, member.id)

    # Get POST data
    cat = None
    hours = 0
    
    # Attempt to get the task category from the given name, for the current group
    try:           
        cat = models.TaskCategory.objects.filter(group = group).get(categoryName = request.POST['task'])
        hours = request.POST['hours']
    except:
        print("Failed to get POST component", request.POST['hours'], request.POST['task'])
        return HttpResponseRedirect(reverse("tracker_app:groupmemdash", args=(group.id, member.id)))


    # Create time entry and save it
    entry = models.MemberEntry(hoursSpent = hours, groupMember = member, category = cat)
    entry.save()

    print("Added time log for ", member.id, " with ", hours, " in category ", cat.categoryName)

    # Go back to group page
    return HttpResponseRedirect(reverse("tracker_app:groupmemdash", args=(group.id, member.id)))