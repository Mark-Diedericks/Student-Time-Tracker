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


def addrole(request, group_id):
    if request.method != 'POST':
        return JsonResponse({ 'status': 'bad' })

    try:
        role_name = request.POST['newRoleName']             # Get name of new role
        g = models.Group.objects.get(pk = group_id)
        role = models.MemberRole(name=role_name, is_owner=False, is_leader=False, group = g)
        role.save()                                         # Create the new role, no special permissions
    except:
        return JsonResponse({ 'status': 'bad' })

    return JsonResponse({'status': 'ok',  'id': role.pk,  'name': role.name}) # Return a JSON response with details of the role



def setroles(request, group_id, mem_id):
    if request.method != 'POST':
        return JsonResponse({ 'status': 'bad' })


    try:    
        selected_roles = request.POST.getlist('selectedRoles')  # Get list of selected roles
        print("Roles: ", request.POST.getlist('selectedRoles'))

        g = models.Group.objects.get(pk = group_id)
        mem = models.GroupMember.objects.get(id = mem_id)
        roles = list(models.MemberRole.objects.filter(group = g))

        req_ref = False                                 # Whether a page refresh is required (changed abilities)

        og_roles = list(mem.roles.all())
        mem.roles.clear()                               # Remove all roles from the user, to add them back in
        rArr = []                                       # Get the names of each role the member has

        # Add back in selected roles and create prettyroles
        for r in roles:
            if str(r.pk) in selected_roles:
                if (r not in og_roles) and (r.is_owner or r.is_leader):
                    req_ref = True                      # Added owner/leader role, thus refresh

                mem.roles.add(r)                        # Add back in the selected roles
                rArr.append(r.name)
            else:
                if (r in og_roles) and (r.is_owner or r.is_leader):
                    req_ref = True                      # Removed owner/leader role, thus refresh

        # Set the pretty names for roles and member name
        prettyroles = ', '.join(rArr)
    except:
        return JsonResponse({ 'status': 'bad' })

    return JsonResponse({'status': 'ok', 'refresh': req_ref, 'prettyroles': prettyroles})