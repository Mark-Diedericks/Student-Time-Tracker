from django.db import models
from django.contrib.auth.models import User

from django.contrib.postgres.fields import ArrayField
from django.core.validators import int_list_validator


# Create your models here.
class GroupMember(models.Model):
    ## user attribute (not quite sure how to store. models.User()? models.ForeignKey(User())?)
    person = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Role(models.IntegerChoices):
        ADMIN = 0,
        LEADER = 1,
        DEVELOPER = 2,
        
    roles = models.CharField(validators=int_list_validator)
    

class MemberEntry(models.Model):
    groupMember = models.ForeignKey(GroupMember)
    hoursSpent = models.IntegerField()


class Group(models.Model):
    groupName = models.CharField(max_length = 30)
    unitCode = models.CharField(max_length = 7)

    members = models.ManyToManyField(GroupMember)
    tasks = models.ManyToManyField(TaskCategory)


class TaskCategory(models.Model):
    categoryName = models.CharField(max_length = 30)
    description = models.TextField()
    submitted = models.BooleanField()
    submittedBy = models.ForeignKey(MemberEntry)
    date = models.DateField()