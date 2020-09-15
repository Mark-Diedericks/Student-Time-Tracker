from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect

# Create your views here.
def index(request):
    # https://docs.djangoproject.com/en/3.1/topics/auth/default/#auth-web-requests

    if (request.user is not None) and (request.user.is_authenticated):
        return redirect('dashboard/')      # We have a user, goto dashboard
    else:
        return redirect('login/')          # We don't have a user, goto login




def login(request):
    return HttpResponse('Login page')




def userdash(request):
    if (request.user is None) or (not request.user.is_authenticated):       # Always ensure we have a user
        return redirect('login/')




    return HttpResponse("User dashboard")




def groupdash(request, group_id):
    if (request.user is None) or (not request.user.is_authenticated):       # Always ensure we have a user
        return redirect('login/')




    return HttpResponse("Group dashboard")