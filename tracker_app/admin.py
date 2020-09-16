from django.contrib import admin
from tracker_app import models

# Register your models here.
admin.site.register(models.GroupMember)
admin.site.register(models.TaskCategory)
admin.site.register(models.MemberEntry)
admin.site.register(models.Group)