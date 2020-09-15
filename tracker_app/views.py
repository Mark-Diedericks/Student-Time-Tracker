from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def login(request):
    return HttpResponse("Login page!")      # Pretty sure django already has a login page built-in so this is redundant...

def userdash(request):
    return HttpResponse("User dashboard")

def groupdash(request):
    return HttpResponse("Group dashboard")