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



##### USER DASH ######
def userdash(request):
    staff = utils.is_staff(request.user)
   

    try:
        all_members = list(models.GroupMember.objects.all())    # Get all members
        mems = []                                               # For normal users (tutor/student), display their groups

        # (GroupMember, is_owner) array of all GroupMembers associated with user
        for mem in all_members:
            if mem.person == request.user: 
                owner = utils.is_owner(mem)
                if not((datetime.today().strftime('%Y-%m-%d') >= mem.group.expiry.strftime('%Y-%m-%d')) and owner):  # check if the group has expired. might think about permanently deleting data from the backend in future should it become necessary
                    mems.append((mem, "0" in mem.roles))

    except:
        raise Http404("Could not get User's groups")
    else:
        return render(request, 'userdash.html', {'members': mems, "is_staff": staff, 'title': ""})