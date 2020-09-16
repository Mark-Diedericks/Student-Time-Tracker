from django.db import models
from django.contrib.auth.models import User
from django.core.validators import int_list_validator


# Create your models here.

class Group(models.Model):
    groupName = models.CharField(max_length = 30)
    unitCode = models.CharField(max_length = 7)

class GroupMember(models.Model):
    person = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    roles = models.CharField(validators=[int_list_validator], max_length=10)

    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)
    

class MemberEntry(models.Model):
    groupMember = models.ForeignKey(GroupMember, on_delete=models.SET_NULL, null=True, blank=True)
    hoursSpent = models.IntegerField()



class TaskCategory(models.Model):
    categoryName = models.CharField(max_length = 30)
    description = models.TextField()
    submitted = models.BooleanField()
    submittedBy = models.ForeignKey(MemberEntry, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField()

    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)
