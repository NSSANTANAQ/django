from django.urls import path
from . import views
from .views import UserListCreateAPIView,login_view,RegistrarSuscripcionView

urlpatterns = [
    # Define tus endpoints aquí
    path('users/', UserListCreateAPIView.as_view(), name='user-list-create'),
    path('login_api/', login_view, name='login_api'),
    path('registrar-suscripcion/', RegistrarSuscripcionView.as_view(), name='registrar_suscripcion'),
]