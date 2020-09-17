from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in!')
            #Needs to be changed from register to dashboard once user is done
            response = redirect('login')
            return response
    else:
        form = UserRegisterForm()
    return render(request,'users/register.html', {'form': form})

#Decorator - adds functionality to our profile view - user must be logged in
@login_required
def profile(request):
    return render(request,'users/profile.html')