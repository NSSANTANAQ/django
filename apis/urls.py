from django.urls import path
from . import views
from .views import UserListCreateAPIView

urlpatterns = [
    # Define tus endpoints aquí
    path('users/', UserListCreateAPIView.as_view(), name='user-list-create'),
]