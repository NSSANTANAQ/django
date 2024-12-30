import os

from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from firebase_admin import messaging

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
    tokens = [suscripcion.token for suscripcion in subscriptions if suscripcion.token]

    if not tokens:
        print("No hay tokens registrados para enviar notificaciones.")
        return

    message = messaging.MulticastMessage(
        notification=messaging.Notification(
            title=payload.get("title"),
            body=payload.get("body"),
        ),
        tokens=tokens,
        data={"url": payload.get("url")},  # Información adicional opcional
    )

    response = messaging.send_multicast(message)
    print(f"Notificaciones enviadas: {response.success_count}, fallidas: {response.failure_count}")

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



def probar_notificacion(request, noticia_id):
    noticia = get_object_or_404(Noticia, pk=noticia_id)
    resultados = noticia
    return JsonResponse({"resultados": resultados})


def enviar_notificacion_prueba(request):
    # Obtiene los tokens de las suscripciones
    subscriptions = Suscripcion.objects.all()
    tokens = [s.token for s in subscriptions if s.token]

    if not tokens:
        messages.error(request, "No hay tokens registrados para enviar notificaciones.")
        return redirect('admin_noticias')  # Ajusta al nombre de tu vista principal

    # Enviar notificaciones
    message = messaging.MulticastMessage(
        notification=messaging.Notification(
            title="Prueba de Notificación",
            body="Esta es una notificación de prueba desde Django.",
        ),
        tokens=tokens,
    )

    response = messaging.send(message)
    messages.success(request, f"Notificaciones enviadas: {response.success_count}, fallidas: {response.failure_count}")
    return redirect('admin_noticias')  # Ajusta al nombre de tu vista principal