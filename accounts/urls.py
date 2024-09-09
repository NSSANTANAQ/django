from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.login_view, name='login'),

    path('signup/', views.signup_view, name='signup'),
    path('proceso_signup/', views.proceso_signup, name='proceso_signup'),
    path('verify_cedula_ruc/', views.verify_cedula_ruc, name='verify_cedula_ruc'),
    path('verificar_conexion_bd/', views.verificar_conexion_bd, name='verificar_conexion_bd'),
    path('registro_usuario_ajax/', views.registro_usuario_ajax, name='registro_usuario_ajax'),

    path('activar_cuenta_modal/<int:pk>/', views.activar_cuenta_modal, name='activar_cuenta_modal'),


    path('logout/', views.custom_logout, name='logout'),
]