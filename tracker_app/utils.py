from datetime import datetime
from datetime import timedelta
from os import times
from tracker_app.models import SubmittedPeriod

from django.contrib.auth.models import User
from tracker_app import models
import csv, io

ROLES_DICT = {"0": "Owner",
            "1": "Leader",
            "2": "Member",} ### TODO, add more roles

class TimeStruct:
    def __init__(self, groupObj, sname, fname, sdate, edate, isat = False):
        self.simplename = sname
        self.fullname = fname

        self.start = sdate
        self.end = edate

        self.isalltime = isat

        self.members = []
        self.tasks = {}

        # Check if the week should be flagged as submitted
        try:
            sDateStr = datetime.strptime(sdate, "%d/%m/%Y").strftime("%Y-%m-%d")
            eDateStr = datetime.strptime(edate, "%d/%m/%Y").strftime("%Y-%m-%d")

            sp = SubmittedPeriod.objects.get(group=groupObj).get(startDate=sDateStr).get(endDate=eDateStr)
            self.submitted = (sp is not None)
        except:
            self.submitted = False

        #self.submitted = (self.submitted) or (endDate < todayDate)


    def add_member(self, mem, tasks):
        for t in tasks:
            # Add the task entry to the member
            mem.add_task(t)

            # Make sure the group has the task registered
            if not (t.taskname in self.tasks):
                self.tasks[t.taskname] = 0
            
            # Add task to group total
            self.tasks[t.taskname] += t.totaltime

        self.members.append(mem)

class MemberStruct:
    def __init__(self, mem, vis):
        self.member = mem
        self.totaltime = 0
        self.visible = vis

        # Get the names of each role the member has
        roles = []
        for r in mem.roles.split(','):
            if r in ROLES_DICT:
                roles.append(ROLES_DICT[r])

        # Set the pretty names for roles and member name
        self.prettyroles = ', '.join(roles)
        self.prettyname = mem.person.get_full_name

        self.tasks = []

    def add_task(self, task):
        # Save the task and add it to the member's total time
        self.tasks.append(task)
        self.totaltime += task.totaltime


class TaskStruct:
    def __init__(self, task, entries):
        self.taskObject = task
        self.taskname = task.categoryName

        self.taskEntries = entries
        self.totaltime = 0

        # Calculate the total time for the given task
        for ent in list(entries):
            self.totaltime += ent.hoursSpent




def get_weeks_entries(group, members, tasks, user_mem):
    sd = datetime.combine(group.created, datetime.min.time())
    ed = datetime.combine(datetime.today(), datetime.min.time())

    start = (sd - timedelta(days = sd.weekday()))    # Get monday of week when group was created
    end = (ed - timedelta(days = ed.weekday()))    # Get monday of current week

    date = start
    step = timedelta(days=7)
    idx = 1

    # Individual weeks
    weeks = []
    while (date <= end):
        ss = date
        es = date + timedelta(days = 6)

        sname = "Week {}".format(idx)
        fname = "{} - {}".format(ss.strftime("%d/%m/%Y"), es.strftime("%d/%m/%Y"))

        # Create the time struct for the current time period
        s_time = TimeStruct(group, sname, fname, ss.strftime("%d/%m/%Y"), es.strftime("%d/%m/%Y"))

        # Get the times relevant to the current time period
        get_times(s_time, ss, es, members, tasks, user_mem)
        weeks.append(s_time)
        
        date += step
        idx += 1


    # All time
    sname = "All time"
    fname = "{} - {}".format(sd.strftime("%d/%m/%Y"), ed.strftime("%d/%m/%Y"))

    # Create the time struct for the all time period
    s_alltime = TimeStruct(group, sname, fname, sd.strftime("%d/%m/%Y"), ed.strftime("%d/%m/%Y"), True)

    # Get the times relevant to the all time period
    get_times(s_alltime, sd, ed, members, tasks, user_mem)
    weeks.append(s_alltime)

    return weeks

def get_times(s_time, start, end, members, tasks, user_mem):
    for m in members:
        # Get entries from the member, for the group, for the giveen time period
        entries = models.MemberEntry.objects.filter(groupMember = m)
        ent = entries.filter(entered__range=[start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")])

        # Whether or not the times should be shown to the logged in user
        should_show = (m ==  user_mem) or is_owner(user_mem)

        # Append total task times, associated with member
        s_mem = MemberStruct(m, should_show)
        s_time.add_member(s_mem, get_totals(ent, tasks))



def get_totals(entries, tasks):
    s_tasks = []

    # Calculate total time for each task
    for t in tasks:
        s_task = TaskStruct(t, entries.filter(category = t))
        s_tasks.append(s_task)

    return s_tasks







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