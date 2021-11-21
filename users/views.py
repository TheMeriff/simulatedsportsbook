from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.views import LogoutView
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
# Create your views here.
from users.services.user_account_service import UserAccountService


def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        form.clean()
        user = request.user
        login(request, user=user)
        return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', context={'form': form})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            UserAccountService.create_account_association(username)
            messages.success(request, f'User account added for {username}.')
            return redirect('index')

    else:
        form = UserCreationForm()

    return render(request, 'users/register.html', context={'form': form})


def logout_request(request):
    form = AuthenticationForm()
    logout(request)
    messages.info(request, "Logged out successfully!")
    return render(request, 'users/login.html', context={'form': form})
