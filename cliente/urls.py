from django.urls import path
from . import views


urlpatterns = [

    path('menu_usuarios/', views.menu_usuarios, name='menu_usuarios'),
    path('usuarios_consulta_cuentas/', views.usuarios_consulta_cuentas, name='usuarios_consulta_cuentas'),
    path('usuarios_consulta_cuentas_detalle/<int:cuenta_id>', views.usuarios_consulta_cuentas_detalle, name='usuarios_consulta_cuentas_detalle'),
    path('usuarios_perfil/', views.usuarios_perfil, name='usuarios_perfil'),


]