from django.db import models
from django.contrib.auth.models import User
from django.core.validators import int_list_validator

from datetime import datetime, timedelta


# Create your models here.

class Group(models.Model):
    groupName = models.CharField(max_length = 30)
    unitCode = models.CharField(max_length = 7)
    
    created = models.DateField(default=datetime.today)
    expiry = models.DateField(default= datetime.today() + timedelta(days=16 * 7))   # 16 weeks by default, needs clarification with Dex


class MemberRole(models.Model):
    name = models.CharField(max_length = 30)

    is_owner = models.BooleanField()
    is_leader = models.BooleanField()

    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)


class GroupMember(models.Model):
    #roles = models.CharField(validators=[int_list_validator], max_length=10)        # Will be the ID's (pk) of MemberRole objects
    roles = models.ManyToManyField(MemberRole)

    person = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)


class TaskCategory(models.Model):
    categoryName = models.CharField(max_length = 30)
    description = models.TextField()
    submitted = models.BooleanField()

    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)


class MemberEntry(models.Model):
    hoursSpent = models.IntegerField()
    entered = models.DateField(default=datetime.today)

    groupMember = models.ForeignKey(GroupMember, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(TaskCategory, on_delete=models.CASCADE, null=True, blank=True)


class SubmittedPeriod(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)

    startDate = models.DateField(default=datetime.today)
    endDate = models.DateField(default=datetime.today)

class ReportIssue(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
    groupMember = models.ForeignKey(GroupMember, on_delete=models.CASCADE, null=True, blank=True)
    title = models.TextField()
    description = models.TextField()
    dateSubmitted = models.DateField(default=datetime.today)



