
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('menu_admin/', views.menu_admin, name='menu_admin'),
    path('admin_noticias/', views.admin_noticias, name='admin_noticias'),
    path('subir-imagen/<int:noticia_id>/', views.subir_imagen, name='subir_imagen'),
    path('probar_notificacion/<int:noticia_id>/', views.prueba_notificacion, name='probar_notificacion'),
]
