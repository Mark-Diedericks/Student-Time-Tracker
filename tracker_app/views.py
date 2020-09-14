from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def login(request):
    return render(request, 'trackerApp/login.html', {'title': 'Log in'})

#Sign up 
def signUp(request):
    return render(request, 'trackerApp/signUp.html', {'title': 'Sign Up'})
