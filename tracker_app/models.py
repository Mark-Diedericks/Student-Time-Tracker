from django.db import models
from django.contrib.auth.models import User
from django.core.validators import int_list_validator


# Create your models here.

class Group(models.Model):
    groupName = models.CharField(max_length = 30)
    unitCode = models.CharField(max_length = 7)

class GroupMember(models.Model):
    roles = models.CharField(validators=[int_list_validator], max_length=10)

    person = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)

class TaskCategory(models.Model):
    categoryName = models.CharField(max_length = 30)
    description = models.TextField()
    submitted = models.BooleanField()
    date = models.DateField()

    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)

class MemberEntry(models.Model):
    hoursSpent = models.IntegerField()

    groupMember = models.ForeignKey(GroupMember, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(TaskCategory, on_delete=models.SET_NULL, null=True, blank=True)