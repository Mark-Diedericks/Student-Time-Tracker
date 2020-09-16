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




def login(request):
    return render(request, 'trackerApp/login.html', {'title': 'Log Ins'})

#Sign up 
def signUp(request):
    return render(request, 'trackerApp/signUp.html', {'title': 'Sign Up'})




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




def groupdash(request, group_id):
    if (request.user is None) or (not request.user.is_authenticated):       # Always ensure we have a user
        return redirect('/login/')

    # Check if user is staff, temp TODO
    staff = request.user.groups.filter(name = "Editors").exists()

    try:                                        # Attempt to get the group from the primary-key (id)
        g = models.Group.objects.get(pk=group_id)
        members = list(models.GroupMember.objects.filter(group = g))

    except:                                     # Group doesn't exist, go back to userdash 
        print("Group does not exist ", group_id)
        return redirect('/dashboard/')

    else:                                       # Group was found, 
        return render(request, 'groupdash.html', {'group': g, 'members': members, 'is_staff': staff, 'title': g.groupName})


def CreateGroup(request):
    form = forms.GroupForm()
    context = {'form':form}
    return render(request,'creategroup.html',context)
