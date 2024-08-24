from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),  # Usar CustomLoginView para /login/
    path('signup/', views.signup_view, name='signup'),
]