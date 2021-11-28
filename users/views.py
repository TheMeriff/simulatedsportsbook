from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
# Create your views here.
from users.services.user_account_service import UserAccountService


def login_request(request):
    if request.method == 'POST':
        user = request.user
        if not user.is_anonymous:
            login(request, user=user)
            return redirect('index')
        else:
            return render(request, 'registration/login.html')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', context={'form': form})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email_address = form.data.get('email_address')
            UserAccountService.create_account_association(username, email_address)
            messages.success(request, f'User account added for {username}.')
            login(request, User.objects.get(username=username))
            return redirect('index')

    else:
        form = UserCreationForm()

    return render(request, 'users/register.html', context={'form': form})


def logout_request(request):
    form = AuthenticationForm()
    logout(request)
    messages.info(request, "Logged out successfully!")
    return render(request, 'registration/login.html', context={'form': form})
