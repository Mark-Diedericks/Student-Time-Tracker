from tracker_app.models import SubmittedPeriod
from django.urls import reverse
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import redirect, render, get_object_or_404

from tracker_app import forms
from tracker_app import models
from tracker_app import utils

import csv, io
from django.contrib import messages

from datetime import datetime



##### GROUP DASH ######
def groupdash(request, group_id, mem_id):

    staff = utils.is_staff(request.user)

    mem = None
    user_mem = None


    # Attempt to get the group, group's members and group's tasks
    try:
        g = models.Group.objects.get(pk = group_id)
        mems = list(models.GroupMember.objects.filter(group = g))
        tasks = list(models.TaskCategory.objects.filter(group = g))
    except:                                     # Group doesn't exist, go back to userdash 
        print("Group does not exist ", group_id)
        return redirect('/dashboard/')

    try:                                        
        # Get the GroupMember of the select user
        mem = models.GroupMember.objects.filter(group = g).get(pk = mem_id)
    except:                                     # Member does not exist, continue without any selection
        print("Member does not exist ", mem_id)


    # Get user member and check if the user is an 'owner' of the group
    user_mem = utils.get_user_member(mems, request.user)
    owner = utils.is_owner(user_mem)
    leader = utils.is_leader(user_mem)

    # TODO, ensure user can view stuff.
    if (user_mem is not None) and (mem is not None) and (user_mem != mem) and (not owner):
        return HttpResponseRedirect(reverse("tracker_app:groupdash", args=[group_id]))
    
    weeks = utils.get_weeks_entries(g, mems, tasks, user_mem)

    can_log = False         # Can log time if the week isn't submitted, view below
    can_sub = leader        # Can submit week logs if they're a leader
    
    # Determine
    # Get the current week (which is where times will be submitted to)
    for w in weeks:
        sDateObj = datetime.strptime(w.start, "%d/%m/%Y")
        eDateObj = datetime.strptime(w.end, "%d/%m/%Y")
        todayDate = datetime.combine(datetime.today(), datetime.min.time())

        # Today's date falls within this week
        if (sDateObj <= todayDate) and (todayDate <= eDateObj):
            can_log = (not w.submitted) # Can log time if the current week is not submitted
            print(can_log)
            break


    # If there is POST data, it is a POST request. Handle logging.
    if (request.method == "POST") and (g is not None) and (user_mem is not None):
        return handle_post(request, g, user_mem, mem_id != -1, can_log, can_sub)
    
    return render(request, 'groupdash.html', {'group': g, 'weeks': weeks, 'tasks': tasks, 'active_member': mem, 'is_staff': staff, 'is_owner': owner, 'is_leader': leader, 'title': g.groupName})





def handle_post(request, group, member, red_mem, can_log, can_sub):
    # If there is no POST data, show the normal groupdash
    if request.method != "POST":
        return groupdash(request, group.id, member.id if red_mem else -1)

    if 'logtime' in request.POST:
        return logtime(request, group, member, red_mem, can_log)

    if 'submittime' in request.POST:
        return submittime(request, group, member, red_mem, can_sub)

    if red_mem:
        return HttpResponseRedirect(reverse("tracker_app:groupmemdash", args=(group.id, member.id)))
    else:
        return HttpResponseRedirect(reverse("tracker_app:groupdash", args=[group.id]))





def submittime(request, g, member, red_mem, can_sub):  
    if can_sub:
        # Attempt to get the task category from the given name, for the current group
        try:           
            start = datetime.strptime(request.POST['start'], "%d/%m/%Y")
            end = datetime.strptime(request.POST['end'], "%d/%m/%Y")

            sp = models.SubmittedPeriod(group = g, startDate = start, endDate = end)
            sp.save()
        except:
            print("Failed to get POST component", request.POST['start'], request.POST['end'])

    if red_mem:
        return HttpResponseRedirect(reverse("tracker_app:groupmemdash", args=(g.id, member.id)))
    else:
        return HttpResponseRedirect(reverse("tracker_app:groupdash", args=[g.id]))





def logtime(request, group, member, red_mem, can_log):   
    if can_log:
        # Get POST data
        cat = None
        hours = 0

        # Attempt to get the task category from the given name, for the current group
        try:           
            cat = models.TaskCategory.objects.filter(group = group).get(categoryName = request.POST['task'])
            hours = request.POST['hours']
        except:
            print("Failed to get POST component", request.POST['hours'], request.POST['task'])
            
            if red_mem:
                return HttpResponseRedirect(reverse("tracker_app:groupmemdash", args=(group.id, member.id)))
            else:
                return HttpResponseRedirect(reverse("tracker_app:groupdash", args=[group.id]))


        # Create time entry and save it
        entry = models.MemberEntry(hoursSpent = hours, groupMember = member, category = cat)
        entry.save()

        print("Added time log for ", member.id, " with ", hours, " in category ", cat.categoryName)


    # Go back to group page
    if red_mem:
        return HttpResponseRedirect(reverse("tracker_app:groupmemdash", args=(group.id, member.id)))
    else:
        return HttpResponseRedirect(reverse("tracker_app:groupdash", args=[group.id]))