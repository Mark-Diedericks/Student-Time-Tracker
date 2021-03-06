from django.urls import reverse
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import redirect, render, get_object_or_404

from tracker_app import forms
from tracker_app import models
from tracker_app import utils

import csv, io
from django.contrib import messages



##### ADD MEMBER ######
def addmember(request, group_id):
    # Only staff can add a member to an existing group
    if not utils.is_staff(request.user):
        return HttpResponseRedirect(reverse("tracker_app:groupdash", args=[group_id]))


    if request.method == 'POST':

        # Members textbox
        mem_text = request.POST['membersField']

        # Members CSV upload
        try:
            mem_file = request.FILES['file']
        except:
            print('No file given')
            mem_file = None

        # Attempt to get the group
        try:
            g = models.Group.objects.get(pk = group_id)
        except:                                     # Group doesn't exist, go back to userdash 
            print("Group does not exist ", group_id)

        entries = []
        # Add entries from textbox
        for line in mem_text.splitlines():
            row = line.split(',')
            if len(row) >= 4:
                entries.append(row)

        # Attempt to add all members, create new if not existing
        for entry in entries:
            try:
                def_role = list(models.MemberRole.objects.filter(group = g).filter(name = entry[0].strip()))[0]
            except:
                def_role = models.MemberRole.objects.filter(group = g).filter(name = "Member").first()
            uname_str = entry[1].strip()
            fname_str = entry[2].strip()
            lname_str = entry[3].strip()

            # Attempt to get User object from given username
            try:  
                p = User.objects.get(username = uname_str)
            except:         # If user does not exist, create it
                # Create a new user with default password
                p = User(username = uname_str, password = utils.default_password())
                p.first_name = fname_str
                p.last_name = lname_str
                p.save()

            # Create the new GroupMember model the user
            mem = models.GroupMember(person = p, group = g)
            mem.save()
            mem.roles.add(def_role)
        
        return HttpResponseRedirect(reverse("tracker_app:groupdash", args=[group_id]))
    else:
        return render(request,'add_member_group.html',{'group_id': group_id})
