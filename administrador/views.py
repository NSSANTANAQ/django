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
from django.contrib import messages
from threading import Thread
def es_admin(user):
    return user.is_authenticated and user.is_staff

# Vista protegida para administradores
@user_passes_test(es_admin, login_url='/cliente/menu_cliente')
def menu_admin(request):
    # Lógica del menú de administrador
    return render(request, 'menu_admin.html')

def enviar_notificaciones_async(subscriptions, payload):
    for subscription in subscriptions:
        send_push_notification(subscription, payload)

def admin_noticias(request):
    if request.method == 'POST':
        noticia_form = NoticiaForm(request.POST, request.FILES)

        if noticia_form.is_valid():
            noticia = noticia_form.save()

            archivos = request.FILES.getlist('imagenes')
            for archivo in archivos:
                ImagenNoticia.objects.create(noticia=noticia, imagen=archivo)

            # Envío de notificaciones push
            payload = {
                "title": noticia.titulo,
                "body": noticia.subtitulo,
                "url": f"https://serviciosenlinea.epmapas.gob.ec/administrador/admin_noticias/{noticia.id}",
            }
            subscriptions = Suscripcion.objects.all()
            Thread(target=enviar_notificaciones_async, args=(subscriptions, payload)).start()

            messages.success(request, "Noticia creada y notificaciones enviadas correctamente.")
            return redirect('admin_noticias')
    else:
        noticia_form = NoticiaForm()
        result = Noticia.objects.all()

    return render(request, 'admin_noticias.html', {
        'noticia_form': noticia_form,
        'result': result,
    })

def subir_imagen(request, noticia_id):
    if request.method == 'POST':
        noticia = get_object_or_404(Noticia, id=noticia_id)
        archivo = request.FILES['file']
        ImagenNoticia.objects.create(noticia=noticia, imagen=archivo)
        return JsonResponse({'mensaje': 'Imagen subida correctamente.'}, status=201)

    return JsonResponse({'error': 'Método no permitido.'}, status=405)


def send_push_notification(subscription, payload):
    try:
        print("Sending notification with payload:", payload)  # Verificar el contenido del payload
        webpush(
            subscription_info={
                "endpoint": subscription.endpoint,
                "keys": {
                    "p256dh": subscription.p256dh,
                    "auth": subscription.auth,
                },
            },
            data=json.dumps(payload),  # Convertimos a JSON
            vapid_private_key=settings.VAPID_PRIVATE_KEY,
            vapid_claims={"sub": settings.VAPID_EMAIL},
        )
    except WebPushException as ex:
        print(f"Error enviando notificación: {str(ex)}")


def probar_notificacion(request, noticia_id):
    noticia = get_object_or_404(Noticia, pk=noticia_id)
    resultados = send_push_notification(noticia)
    return JsonResponse({"resultados": resultados})