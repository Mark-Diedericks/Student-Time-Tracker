from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def login(request):
    return HttpResponse("<h1>Project Tracker Login page</h1>")

#Sign up 
def signUp(request):
    return HttpResponse("<h1>Sign Up Page</h1>")
