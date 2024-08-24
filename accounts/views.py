from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignUpForm,LoginForm
from django.contrib.auth import views as auth_views
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Cambia 'home' por la URL a la que quieras redirigir al usuario después del login
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

