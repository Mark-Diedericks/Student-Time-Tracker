
from django.contrib.auth.models import User
from tracker_app import models
import csv, io



def is_staff(user):
    """
    Check if a given User (Django) is a staff member
    """
    # Check if user is staff, temp TODO
    return user.groups.filter(name = "Editors").exists()

def is_owner(member):
    """
    Checks if a given GroupMember has the owner (0) role
    """
    if member is None:
        return False

    return "0" in member.roles


def get_user_member(members, user):
    """
    Gets the GroupMember associated with a User (Django) if it exists within the collection
    """
    # Identify the GroupMember associated witht he User
    for mem in members:
        if mem.person == user:
            return mem

    return None


def get_member_times(members, tasks, user_mem):   
    times = []

    # For each GroupMember, select calculate their total times for each task category and produce the member array
    for m in members:
        m_tot = []
        entries = models.MemberEntry.objects.filter(groupMember = m)

        # Calculate total time for each task
        for t in tasks:
            val = 0
            for ent in list(entries.filter(category = t)):
                val += ent.hoursSpent

            if  (m == user_mem) or is_owner(user_mem):
                m_tot.append(val)
            else:
                m_tot.append(" ")

        # Append total task times, associated with member
        times.append((m, m_tot))

    return times

def default_password():
    """
    Returns a default password for auto-user-creation
    """
    return "abc123"