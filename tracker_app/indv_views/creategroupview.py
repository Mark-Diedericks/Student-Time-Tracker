from django.urls import reverse
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import redirect, render, get_object_or_404

from tracker_app import forms
from tracker_app import models
from tracker_app import utils

import csv, io
from django.contrib import messages



##### GROUP CREATE ######
def creategroup(request):
    # Only staff can create groups
    if not utils.is_staff(request.user):
        return redirect("/dashboard/")


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
            # TODO move to group creation
            # Add default roles to a group if it has none
            dev = models.MemberRole(name="Developer", is_owner=False, is_leader=False, group = g)
            dev.save()

            lead = models.MemberRole(name="Leader", is_owner=False, is_leader=True, group = g)
            lead.save()

            own = models.MemberRole(name="Owner", is_owner=True, is_leader=False, group = g)
            own.save()
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
        owner_user = models.GroupMember(person=request.user, group=g)
        owner_user.save()
        owner_user.roles.add(own)
        
        for entry in entries:
            try:
                def_role = list(models.MemberRole.objects.filter(group = g).filter(name = entry[0].strip()))[0]
            except:
                def_role = dev
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
            

        
        return redirect("/dashboard/")
    else:
        return render(request,'creategroup.html')
