from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignUpForm,LoginForm
from django.contrib.auth import views as auth_views
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')  # Redirige a la página de inicio después de registrarse
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    return render(request, 'accounts/login.html')  # Asegúrate de tener el template en esta ruta
class CustomLoginView(auth_views.LoginView):
    template_name = 'accounts/login.html'
    authentication_form = LoginForm