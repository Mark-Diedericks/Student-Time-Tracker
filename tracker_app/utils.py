from datetime import datetime
from datetime import timedelta
from os import times

from django.contrib.auth.models import User
from tracker_app import models
import csv, io


class TimeStruct:

    def __init__(self, member, ):

        self.x = 0

def get_weeks_entries(group, members, tasks, user_mem):
    sd = datetime.combine(group.created, datetime.min.time())
    ed = datetime.combine(datetime.today(), datetime.min.time())

    start = (sd - timedelta(days = sd.weekday()))    # Get monday of week when group was created
    end = (ed - timedelta(days = ed.weekday()))    # Get monday of current week

    date = start
    step = timedelta(days=7)

    weeks = []
    while (date <= end):
        ss = date
        es = date + timedelta(days = 6)

        weeks.append(("{} - {}".format(ss.strftime("%d/%m/%Y"), es.strftime("%d/%m/%Y")), get_times(ss, es, members, tasks, user_mem)))
        date += step

    weeks.append(("All Time", get_times(sd, ed, members, tasks, user_mem)))

    return weeks

def get_times(start, end, members, tasks, user_mem):
    times = []

    for m in members:
        entries = models.MemberEntry.objects.filter(groupMember = m)
        ent = entries.filter(entered__range=[start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")])

        should_show = (m ==  user_mem) or is_owner(user_mem)

        # Append total task times, associated with member
        times.append((m, get_totals(ent, tasks, should_show)))

    return times


def get_totals(entries, tasks, should_show):
    totals = []

    # Calculate total time for each task
    for t in tasks:
        val = 0
        for ent in list(entries.filter(category = t)):
            val += ent.hoursSpent
        totals.append(val)
    
    return totals







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

def default_password():
    """
    Returns a default password for auto-user-creation
    """
    return "abc123"