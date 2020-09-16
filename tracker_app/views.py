from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import redirect, render, get_object_or_404

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
    #if (request.user is None) or (not request.user.is_authenticated):       # Always ensure we have a user
    #    return redirect('/login/')

    try:
        #g = list(models.Group.objects.filter(users__contains=request.user))      # Get QuerySet of all groups the user belongs to
        g = ["Group 1", "Group 2", "Group 3", "Group 4", "ABC Group", "DEF Group", "GHI Group", "JKL Group", "Long Name Group Name Long", "Other Group"]
    except:
        raise Http404("Could not get User's groups")
    else:
        return render(request, 'userdash.html', {'groups': g})




def groupdash(request, group_id):
    #if (request.user is None) or (not request.user.is_authenticated):       # Always ensure we have a user
    #    return redirect('/login/')
    
    if True:
        return render(request, 'groupdash.html', {'group': group_id})

    try:                                        # Attempt to get the group from the primary-key (id)
        g = models.Group.objects.get(pk=group_id)

    except:                                     # Group doesn't exist, go back to userdash 
        print("Group does not exist ", group_id)
        return redirect('/dashboard/')

    else:                                       # Group was found, 
        return render(request, 'groupdash.html', {'group': g})
