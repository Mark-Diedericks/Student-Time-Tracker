from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

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

#Changes the user's password to the new entered password
@login_required
def passwordResetLoggedIn(request):
    current_user = request.user
    user_name = current_user.get_username()
    if request.method == 'POST':
        newPass = request.POST['password']
        try:
            if validate_password(newPass, user=current_user, password_validators=None) == None:
                u = User.objects.get(username= user_name)
                u.set_password(newPass)
                u.save()
                return render(request,'users/loggedInPasswordResetDone.html')
        except:
            return render(request,'users/loggedInPasswordResetFail.html')
    return render(request,'users/loggedInPasswordReset.html')