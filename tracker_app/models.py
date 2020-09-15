from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField


# Create your models here.
class GroupMember(models.Model):
    ## user attribute (not quite sure how to store. models.User()? models.ForeignKey(User())?)
    roles = models.ArrayField(
        models.CharField(max_length = 20),
        size = 10, # at most you can have 10 roles (had to specify this param)
    )
    

class MemberEntry(models.Model):
    groupMember = models.ForeignKey(GroupMember)
    hoursSpent = models.IntegerField()


class Group(models.Model):
    groupName = models.CharField(max_length = 30)
    unitCode = models.CharField(max_length = 7)
    members = models.ManyToManyField(User, through = "GroupMember")


class TaskCategory(models.Model):
    categoryName = models.CharField(max_length = 30)
    description = models.TextField()
    submitted = models.BooleanField()
    submittedBy = models.ForeignKey(MemberEntry)
    date = models.DateField()