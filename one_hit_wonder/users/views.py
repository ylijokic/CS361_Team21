from django.shortcuts import render, redirect
# from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm

def register(request):
    # Check if the registration form request is a POST request
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        # Verify registration form has valid input
        if form.is_valid():
            # Adds user to django admin page
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Account created for {username}")
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})
