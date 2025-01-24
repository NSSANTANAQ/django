from django.urls import path
from . import views
from .views import login

urlpatterns = [
    path('login/', views.login_view, name='login'),

    path('signup/', views.signup_view, name='signup'),
    path('proceso_signup/', views.proceso_signup, name='proceso_signup'),
    path('verify_cedula_ruc/', views.verify_cedula_ruc, name='verify_cedula_ruc'),
    path('verificar_conexion_bd/', views.verificar_conexion_bd, name='verificar_conexion_bd'),
    path('registro_usuario_ajax/', views.registro_usuario_ajax, name='registro_usuario_ajax'),

    path('activar_cuenta_modal/<int:pk>/', views.activar_cuenta_modal, name='activar_cuenta_modal'),

    path('cuenta_activada_exito/', views.cuenta_activada_exito, name='cuenta_activada_exito'),

    path('logout/', views.custom_logout, name='logout'),

    path('recuperar_password/', views.password_reset_request, name="recuperar_password"),
    path('password_reset_confirm/<uidb64>/<token>/', views.my_password_reset_confirm, name='password_reset_confirm'),
    path('password_reset_exito/', views.password_reset_exito, name="password_reset_exito"),
    path('envio_exitoso_enlace_email/', views.envio_exitoso_enlace_email, name="envio_exitoso_enlace_email"),



]