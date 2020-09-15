from django.db import models

# Create your models here.
class Group(models.Model):
    groupName = models.CharField(max_length=30)
    unitCode = models.CharField(max_length=7)

    ## 'users' manytomany field of users

class TaskCategory(models.Model):
    categoryName = models.CharField(max_length=30)
    description = models.CharField(max_length=1000)
    
    submitted = models.BooleanField()