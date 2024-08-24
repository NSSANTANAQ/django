from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),  # Esto vincula la URL /login/ a la vista login_view
]