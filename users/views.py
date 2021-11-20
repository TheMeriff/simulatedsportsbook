from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
# Create your views here.
from users.services.user_account_service import UserAccountService


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
