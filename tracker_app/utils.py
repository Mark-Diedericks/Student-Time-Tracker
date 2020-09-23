
from django.contrib.auth.models import User
from tracker_app import models
import csv, io



def is_staff(user):
    """
    Check if a given User (Django) is a staff member
    """
    # Check if user is staff, temp TODO
    return user.groups.filter(name = "Editors").exists()


def default_password():
    """
    Returns a default password for auto-user-creation
    """
    return "abc123"