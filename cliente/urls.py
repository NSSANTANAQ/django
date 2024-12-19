from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('menu_usuarios/', views.menu_usuarios, name='menu_usuarios'),
    path('usuarios_consulta_cuentas/', views.usuarios_consulta_cuentas, name='usuarios_consulta_cuentas'),
    path('usuarios_consulta_cuentas_detalle/<int:cuenta_id>', views.usuarios_consulta_cuentas_detalle, name='usuarios_consulta_cuentas_detalle'),
    path('usuarios_perfil/', views.usuarios_perfil, name='usuarios_perfil'),
    path('usuarios_noticias/', views.usuarios_noticias, name='usuarios_noticias'),
    path('usuarios_cambiar_password/', views.usuarios_cambiar_password, name='usuarios_cambiar_password'),
    path('usuarios_cambiar_password_exito/', views.usuarios_cambiar_password_exito, name='usuarios_cambiar_password_exito'),

    path('usuarios_reportes/', views.usuarios_reportes, name='usuarios_reportes'),
]