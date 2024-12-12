from django.urls import path
from . import views
from .views import UserListCreateAPIView,login_view

urlpatterns = [
    # Define tus endpoints aquí
    path('users/', UserListCreateAPIView.as_view(), name='user-list-create'),
    path('login_api/', login_view, name='login_api'),
]