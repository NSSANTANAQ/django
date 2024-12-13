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

            enviar_notificacion(noticia)

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



def enviar_notificacion(title, body, url):
    payload = {
        "title": title,
        "body": body,
        "url": url,
    }
    suscripciones = Suscripcion.objects.all()
    resultados = []
    for suscripcion in suscripciones:
        try:
            webpush(
                subscription_info={
                    "endpoint": suscripcion.endpoint,
                    "keys": {
                        "p256dh": suscripcion.p256dh,
                        "auth": suscripcion.auth,
                    },
                },
                data=json.dumps(payload),
                vapid_private_key=settings.VAPID_PRIVATE_KEY,
                vapid_claims=settings.VAPID_CLAIMS,
            )
            resultados.append(f"Notificación enviada a: {suscripcion.endpoint}")
        except WebPushException as ex:
            resultados.append(f"Error enviando a {suscripcion.endpoint}: {str(ex)}")
    return resultados

def probar_notificacion(request, noticia_id):
    noticia = get_object_or_404(Noticia, pk=noticia_id)
    resultados = enviar_notificacion(noticia)
    return JsonResponse({"resultados": resultados})