from django.db import models
from django.contrib.auth.models import User
from django.core.validators import int_list_validator

from datetime import datetime


# Create your models here.

class Group(models.Model):
    groupName = models.CharField(max_length = 30)
    unitCode = models.CharField(max_length = 7)
    
    created = models.DateField(default=datetime.today)

class GroupMember(models.Model):
    roles = models.CharField(validators=[int_list_validator], max_length=10)

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