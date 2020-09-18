from django.urls import reverse
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required

from tracker_app import forms
from tracker_app import models

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
    # Check if user is staff, temp TODO
    staff = request.user.groups.filter(name = "Editors").exists()

    try:
        all_members = list(models.GroupMember.objects.all())    # Get all members
        mems = []                                               # For normal users (tutor/student), display their groups

        # (GroupMember, is_owner) array of all GroupMembers associated with user
        for mem in all_members:
            if mem.person == request.user:
                mems.append((mem, "0" in mem.roles))

    except:
        raise Http404("Could not get User's groups")
    else:
        return render(request, 'userdash.html', {'members': mems, "is_staff": staff, 'title': ""})


##### GROUP DASH ######
@login_required
def groupdash(request, group_id, mem_id = -1):
    # Check if user is staff, temp TODO
    staff = request.user.groups.filter(name = "Editors").exists()
    mem = None
    user_mem = None
    members = []


    # Attempt to get the group, group's members and group's tasks
    try:
        g = models.Group.objects.get(pk = group_id)
        mems = list(models.GroupMember.objects.filter(group = g))
        tasks = list(models.TaskCategory.objects.filter(group = g))


        # Identify the GroupMember associated witht he User
        for mem in mems:
            if mem.person == request.user:
                user_mem = mem
                break

    except:                                     # Group doesn't exist, go back to userdash 
        print("Group does not exist ", group_id)
        return redirect('/dashboard/')


    # TODO, lock into one user.
    if (mem_id == -1) and (user_mem is not None):
        return redirect("/dashboard/{}/{}".format(group_id, user_mem.id))

    # Determine if the user is an 'owner' of the group
    if user_mem is not None:
        owner = "0" in user_mem.roles
    else:
        owner = False


    # TODO, ensure user can view stuff.
    if (user_mem is not None) and (mem_id != user_mem.id):
        if (not owner):
            return redirect("/dashboard/{}/{}".format(group_id, user_mem.id))

    members = []

    try:                                        
        # Get the GroupMember of the select user
        mem = models.GroupMember.objects.filter(group = g).get(pk = mem_id)
        
        # For each GroupMember, select calculate their total times for each task category and produce the member array
        for m in mems:
            m_tot = []
            entries = models.MemberEntry.objects.filter(groupMember = m)

            # Calculate total time for each task
            for t in tasks:
                val = 0
                for ent in list(entries.filter(category = t)):
                    val += ent.hoursSpent

                if  (m == user_mem) or (owner):
                    m_tot.append(val)
                else:
                    m_tot.append(" ")

            # Append total task times, associated with member
            members.append((m, m_tot))

    except:                                     # Member does not exist, continue without any selection
        print("Member does not exist ", mem_id)
        return redirect("/dashboard/{}/".format(group_id))

    # If there is POST data, it is a logtime request. Handle logging.
    if (request.method == "POST") and (g is not None) and (mem is not None):
        return logtime(request, g, mem)
    
    return render(request, 'groupdash.html', {'group': g, 'members': members, 'tasks': tasks, 'active_member': mem, 'is_staff': staff, 'is_owner': owner, 'title': g.groupName})


@login_required
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
        return redirect("/dashboard/{}/{}".format(group.id, member.id))


    # Create time entry and save it
    entry = models.MemberEntry(hoursSpent = hours, groupMember = member, category = cat)
    entry.save()

    print("Added time log for ", member.id, " with ", hours, " in category ", cat.categoryName)

    # Go back to group page
    return redirect("/dashboard/{}/{}".format(group.id, member.id))


##### GROUP CREATE ######

@login_required
def CreateGroup(request):
    if request.method == 'POST':
        # Group info
        gname = request.POST['groupName']
        gcode = request.POST['unitCode']

        # Members textbox
        mem_text = request.POST['membersField']

        # Members CSV upload
        try:
            mem_file = request.FILES['file']
        except:
            print('No file given')
            mem_file = None

        # Attempt to create the group
        try:
            g = models.Group(groupName = gname, unitCode = gcode)
            g.save()
        except:
            print('Failed to create group', gname, gcode)
            return redirect('/dashboard/')


        entries = []
        # Add entries from textbox
        for line in mem_text.splitlines():
            row = line.split(',')
            if len(row) >= 4:
                entries.append(row)

        # Add entries from file
        if mem_file is not None:
            if mem_file.name.lower().endswith('.csv') or mem_file.name.lower().endswith('.txt'):
                
                data_set = mem_file.read().decode('UTF-8')
                io_string = io.StringIO(data_set)
                next(io_string)

                # Each row correseponds to a user. Attempt to add that user to the corresponding group
                for row in csv.reader(io_string, delimiter=',',quotechar="|"):
                    if len(row) >= 4:
                        entries.append(row)
        
        # Attempt to add all members, create new if not existing
        for entry in entries:
            role_str = entry[0].strip()
            uname_str = entry[1].strip()
            fname_str = entry[2].strip()
            lname_str = entry[3].strip()

            # Attempt to get User object from given username
            try:  
                p = User.objects.get(username = uname_str)
            except:         # If user does not exist, create it
                names = uname_str.split(' ')

                # Create a new user with default password
                p = User(username = uname_str, password = "abc123")     # TODO, defualt password
                p.first_name = fname_str
                p.last_name = lname_str
                p.save()

            # Create the new GroupMember model the user
            mem = models.GroupMember(roles = role_str, person = p, group = g)
            mem.save()

        
        return redirect("/dashboard/")
    else:
        return render(request,'creategroup.html')


