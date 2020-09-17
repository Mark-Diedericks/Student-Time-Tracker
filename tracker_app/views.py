from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import redirect, render, get_object_or_404

from tracker_app import forms
from tracker_app import models

# Create your views here.
def index(request):
    # https://docs.djangoproject.com/en/3.1/topics/auth/default/#auth-web-requests

    if (request.user is not None) and (request.user.is_authenticated):
        return redirect('/dashboard/')      # We have a user, goto dashboard
    else:
        return redirect('/login/')          # We don't have a user, goto login


##### USER REG ######

def login(request):
    return render(request, 'trackerApp/login.html', {'title': 'Log Ins'})

def signUp(request):
    return render(request, 'trackerApp/signUp.html', {'title': 'Sign Up'})


##### GROUP REG ######

def CreateGroup(request):
    form = forms.GroupForm()
    context = {'form':form}
    return render(request,'creategroup.html',context)


##### USER DASH ######

def userdash(request):
    if (request.user is None) or (not request.user.is_authenticated):       # Always ensure we have a user
        return redirect('/login/')

    # Check if user is staff, temp TODO
    staff = request.user.groups.filter(name = "Editors").exists()

    try:
        all_members = list(models.GroupMember.objects.all())    # Get all members
        mems = []                                         # For normal users (tutor/student), display their groups
        for mem in all_members:
            if mem.person == request.user:
                mems.append((mem, "0" in mem.roles))

    except:
        raise Http404("Could not get User's groups")
    else:
        return render(request, 'userdash.html', {'members': mems, "is_staff": staff, 'title': ""})


##### GROUP DASH ######

def groupdash(request, group_id, mem_id = -1):
    if (request.user is None) or (not request.user.is_authenticated):       # Always ensure we have a user
        return redirect('/login/')

    # Check if user is staff, temp TODO
    staff = request.user.groups.filter(name = "Editors").exists()
    mem = None
    user_mem = None


    try:                                        # Attempt to get the group from the primary-key (id)
        g = models.Group.objects.get(pk = group_id)
        members = list(models.GroupMember.objects.filter(group = g))
        tasks = list(models.TaskCategory.objects.filter(group = g))


        for mem in members:
            if mem.person == request.user:
                user_mem = mem
                break
    except:                                     # Group doesn't exist, go back to userdash 
        print("Group does not exist ", group_id)
        return redirect('/dashboard/')


    # TODO, temp, lock into one user.
    if (mem_id == -1) and (user_mem is not None):
        return redirect("/dashboard/{}/{}".format(group_id, user_mem.id))

    # TODO, temp, ensure user can view stuff.
    if (user_mem is not None) and (mem_id != user_mem.id):
        if (not "0" in user_mem.roles):
            return redirect("/dashboard/{}/{}".format(group_id, user_mem.id))

    totals = []

    try:                                        # Attempt to get the active user, if there is any
        mem = models.GroupMember.objects.filter(group = g).get(pk = mem_id)


        entries = models.MemberEntry.objects.filter(groupMember = mem)
        for t in tasks:
            val = 0

            for ent in list(entries.filter(category = t)):
                val += ent.hoursSpent
            
            totals.append(val)

    except:                                     # Member does not exist, continue without any selection
        print("Member does not exist ", mem_id)
        return redirect("/dashboard/{}/".format(group_id))

    if (request.method == "POST") and (g is not None) and (mem is not None):
        return logtime(request, g, mem)
    
    return render(request, 'groupdash.html', {'group': g, 'members': members, 'tasks': tasks, 'totals': totals, 'active_member': mem, 'is_staff': staff, 'title': g.groupName})



def logtime(request, group, member):   
    if (request.user is None) or (not request.user.is_authenticated):       # Always ensure we have a user
        return redirect('/login/')

    if request.method != "POST":
        return groupdash(request, group.id, member.id)

    # Get POST data
    cat = None
    hours = 0
    
    try:           
        cat = models.TaskCategory.objects.get(categoryName = request.POST['task'])
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

    