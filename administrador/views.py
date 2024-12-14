import os

from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import NoticiaForm
from .models import Noticia, ImagenNoticia
from django.shortcuts import render, redirect
from django.http import JsonResponse
from apis.models import Suscripcion
from .forms import NoticiaForm  # Asume que tienes un formulario para Noticia
from django.conf import settings
from pywebpush import webpush, WebPushException
import json
from django.db.models.signals import post_save
from django.dispatch import receiver
import requests
def es_admin(user):
    return user.is_authenticated and user.is_staff

# Vista protegida para administradores
@user_passes_test(es_admin, login_url='/cliente/menu_cliente')
def menu_admin(request):
    # Lógica del menú de administrador
    return render(request, 'menu_admin.html')


def admin_noticias(request):
    if request.method == 'POST':
        noticia_form = NoticiaForm(request.POST, request.FILES)

        if noticia_form.is_valid():
            # Guardar la noticia
            noticia = noticia_form.save()

            archivos = request.FILES.getlist('imagenes')

            for archivo in archivos:
                ImagenNoticia.objects.create(noticia=noticia, imagen=archivo)


            return redirect('admin_noticias')  # Redirige a la vista de administración de noticias
    else:
        noticia_form = NoticiaForm()
        result = Noticia.objects.all()
    return render(request, 'admin_noticias.html', {
        'noticia_form': noticia_form,'result': result,
    })

def subir_imagen(request, noticia_id):
    if request.method == 'POST':
        noticia = get_object_or_404(Noticia, id=noticia_id)
        archivo = request.FILES['file']
        ImagenNoticia.objects.create(noticia=noticia, imagen=archivo)
        return JsonResponse({'mensaje': 'Imagen subida correctamente.'}, status=201)

    return JsonResponse({'error': 'Método no permitido.'}, status=405)



@receiver(post_save, sender=Noticia)
def send_push_notification(sender, instance, created, **kwargs):
    if created:  # Solo cuando la noticia es creada
        subscriptions = Suscripcion.objects.all()
        for subscription in subscriptions:
            payload = {
                "title": instance.titulo,
                "body": instance.subtitulo,
                "url": "https://https://serviciosenlinea.epmapas.gob.ec/administrador/admin_noticias/" + str(instance.id),  # URL de la noticia
            }
            send_notification(subscription, payload)

def send_notification(subscription, payload):
    try:
        webpush(
            subscription_info={
                "endpoint": subscription.endpoint,
                "keys": {
                    "p256dh": subscription.p256dh,
                    "auth": subscription.auth,
                },
            },
            data=json.dumps(payload),
            vapid_private_key=os.getenv("VAPID_PRIVATE_KEY"),
            vapid_claims={
                "sub": os.getenv("VAPID_EMAIL"),
            },
        )
        print("Notificación enviada con éxito")
    except WebPushException as ex:
        print(f"Error enviando notificación: {ex}")


def probar_notificacion(request, noticia_id):
    noticia = get_object_or_404(Noticia, pk=noticia_id)
    resultados = send_push_notification(noticia)
    return JsonResponse({"resultados": resultados})