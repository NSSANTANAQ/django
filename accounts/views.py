from django.shortcuts import render

def login_view(request):
    return render(request, 'accounts/login.html')  # Asegúrate de tener el template en esta ruta
