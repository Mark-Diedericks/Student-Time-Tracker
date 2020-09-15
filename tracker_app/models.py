from django.db import models
from django.contrib.auth.models import User

# Create your models here.
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

class GroupMember(models.Model):
    ## user attribute (not quite sure how to store. models.User()? models.ForeignKey(User())?)
    person = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    roles = models.ListCharField(
        base_field = models.CharField(max_length = 20),
        size = 10, # at most you can have 10 roles (had to specify this param)
        max_length = 200 # 10 slots * 20 chars
    )

class MemberEntry(models.Model):
    groupMember = models.ForeignKey(GroupMember)
    hoursSpent = models.IntegerField()