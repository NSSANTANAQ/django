from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.conf import settings
from .forms import SignUpForm,LoginForm, ConsultaClienteForm
from django.contrib import messages
from django.contrib.auth import logout
from cliente.models import AdCliente
from django.http import JsonResponse
from django.db import connections, OperationalError
from django.views.decorators.csrf import csrf_exempt
import random
import string
from django.core.mail import send_mail
from .models import ActivationCode
from django.utils.crypto import get_random_string
from django.utils import timezone
from datetime import timedelta
from django.core.mail import BadHeaderError
from django.http import HttpResponse
from django.core.exceptions import ImproperlyConfigured
import socket

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = form.data.get('username')  # Obtenemos el username del formulario sin validarlo aún
        password = form.data.get('password')  # Obtenemos el password del formulario sin validarlo aún

        try:
            # Intentamos obtener el usuario por el username
            user = get_object_or_404(User, username= username)

            # Verificamos si el usuario está activo
            if not user.is_active:

                return redirect('activar_cuenta_modal',  user.pk)

            # Si el usuario está activo, procedemos con la validación del formulario
            if form.is_valid():
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('menu_usuarios')
                else:
                    print("Usuario o contraseña incorrectos")
                    messages.error(request, 'Usuario o contraseña incorrectos.')
            else:
                # Mostrar los errores del formulario
                print(f"Errores del formulario: {form.errors}")
                messages.error(request, 'Formulario no válido.')

        except User.DoesNotExist:
            print("Usuario no encontrado")
            messages.error(request, 'Usuario no encontrado.')

    else:
        form = LoginForm()

    # Renderizamos la página de login en caso de error o GET
    return render(request, 'login.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirige a la página principal o al lugar que prefieras

    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def custom_logout(request):
    logout(request)
    return render(request, 'logout.html')

def proceso_signup(request):
    form = SignUpForm()
    return render(request, 'proceso_signup.html',{'form': form})


@csrf_exempt
def verify_cedula_ruc(request):
    if request.method == 'POST':
        cedula_ruc = request.POST.get('cedula_ruc')
        if cedula_ruc == '999999999':
            return JsonResponse({'status': 'error', 'message': 'Cedula no existe'})

        if cedula_ruc:
            try:
                cursor = connections['railway'].cursor()
                cursor.execute('SELECT * FROM administracion.ad_cliente WHERE cedula_ruc = %s', [cedula_ruc])
                result = cursor.fetchall()

                if result:
                    # Verificar si el correo electrónico está presente
                    name_index = 1
                    email_index = 10  # Asumiendo que el email está en la decima columna

                    if result[0][email_index]:  # Verificar si el campo del email no está vacío

                        return JsonResponse({
                            'status': 'success',
                            'message': 'Exito, puede continuar',
                            'data': list(result),
                            'name': result[0][email_index],
                            'email': result[0][name_index],
                        })
                    else:
                        return JsonResponse({
                            'status': 'warning',
                            'message': 'El correo electrónico no está registrado. Por favor, actualice sus datos en Atención al Cliente.'
                        })

                else:
                    return JsonResponse({'status': 'error', 'message': 'Sin Registros'})

            except Exception as e:
                return JsonResponse({'status': 'error', 'message': 'Servicio no Disponible'})
        else:
            return JsonResponse({'status': 'error', 'message': '¡Ingrese su CI/RUC , porfavor!'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Método no permitido.'})

def verificar_conexion_bd(request):
    try:
        # Intentar conectar a la base de datos 'epmapas'
        cursor = connections['railway'].cursor()

        # Realizar una consulta simple a la tabla administracion.ad_cliente
        cursor.execute('SELECT * FROM administracion.ad_cliente LIMIT 1')
        result = cursor.fetchall()

        # Si se obtuvieron resultados, la conexión es exitosa
        if result:
            return JsonResponse({
                'status': 'success',
                'message': 'Conexión exitosa y datos obtenidos correctamente.',
                'data': result
            })
        else:
            return JsonResponse({
                'status': 'success',
                'message': 'Conexión exitosa, pero no se encontraron datos en la tabla.'
            })

    except OperationalError as e:
        # Si ocurre un error, la conexión falló
        return JsonResponse({
            'status': 'error',
            'message': f'Error de conexión: {str(e)}'
        })

    except Exception as e:
        # Manejo general de excepciones
        return JsonResponse({
            'status': 'error',
            'message': f'Error: {str(e)}'
        })


@csrf_exempt
def registro_usuario_ajax(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Guardar el usuario
            user = form.save(commit=False)
            user.is_active = False  # El usuario no está activo hasta que se active por correo
            user.save()

            # Enviar el correo de activación
            send_activation_email(user)

            return JsonResponse({'status': 'success', 'message': 'Usuario registrado exitosamente.'})
        else:
            # Crear una lista para almacenar los errores
            errors = []
            for field, field_errors in form.errors.items():
                for error in field_errors:
                    # Agregar cada error con el nombre del campo
                    errors.append({'field': 'Alerta', 'message': str(error)})
            return JsonResponse({'status': 'error', 'errors': errors})

    return JsonResponse({'status': 'error', 'message': 'Método no permitido.'})


def generate_activation_code():
    return get_random_string(length=20, allowed_chars=string.ascii_letters + string.digits)

def send_activation_email(user):
    try:
        # Generar un nuevo código de activación
        activation_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        expiration_time = timezone.now() + timedelta(minutes=10)

        # Actualizar o crear un nuevo código de activación
        activation_code_obj, created = ActivationCode.objects.update_or_create(
            username=user.username,
            defaults={
                'email': user.email,
                'code': activation_code,
                'expiration_time': expiration_time
            }
        )

        try:
            send_mail(
                'Código de activación de cuenta',
                f'Estimado Usuario Tu código de activación es: {activation_code}, Inicia Sesión con tu usuario y contraseña para activarlo,'
                f'Si tienes Problemas de Activación comunicate al siguiente correo electrónico, serviciosenlinea@epmapas.gob.ec o al numero 0996884553',
                settings.EMAIL_HOST_USER,
                [user.email],

            )
        except BadHeaderError:
            # Maneja los errores relacionados con encabezados inválidos
            return HttpResponse('Error en el servicio, por favor intente de nuevo más tarde.', status=500)
        except Exception as e:
            # Maneja otros errores relacionados con el envío de correos
            return HttpResponse('Error en el servicio, por favor intente de nuevo más tarde.', status=500)

        # Si todo sale bien, puedes retornar un mensaje de éxito o redirigir al usuario
        return HttpResponse('Código de activación enviado con éxito.')

    except Exception as e:
        # Maneja cualquier otro error en la función
        return HttpResponse('Error en el servicio, por favor intente de nuevo más tarde.', status=500)


def verificar_codigo_activacion(request):
    if request.method == 'POST':
        codigo = request.POST.get('codigo')
        try:
            # Buscar el código de activación en la base de datos
            activation_code = ActivationCode.objects.get(code=codigo)
            if activation_code.is_expired():
                messages.error(request, 'El código ha expirado.')
                return redirect('activar_cuenta_modal')  # Redirige a la misma página

            # Activar el usuario
            user = AdCliente.objects.get(username=activation_code.username)
            user.is_active = True
            user.save()

            # Eliminar el código de activación
            activation_code.delete()
            messages.success(request, 'Usuario activado correctamente.')
            return redirect('login')  # Redirige al login o donde desees

        except ActivationCode.DoesNotExist:
            messages.error(request, 'Código inválido.')
            return redirect('activar_cuenta_modal')  # Redirige a la misma página

    return render(request, 'activar_cuenta_modal.html')


def activar_cuenta_modal(request, pk):
    if request.method == 'POST':
        user = get_object_or_404(User, id=pk)
        codigo = request.POST.get('codigo')
        try:
            activation_code = ActivationCode.objects.get(username=user.username, code=codigo)

            if activation_code.is_expired():
                messages.error(request,
                               'El código ha expirado se ha enviado un nuevo código de Activación, revisa tu correo electrónico')
                send_activation_email(user)

            else:
                # Activar el usuario
                user = User.objects.get(username=user.username)
                user.is_active = True
                user.save()

                # Eliminar el código de activación
                activation_code.delete()

                # Redirigir a la página principal
                return redirect('cuenta_activada_exito')

        except ActivationCode.DoesNotExist:
            messages.error(request, 'Código inválido.')

    return render(request, 'activar_cuenta_modal.html')

def cuenta_activada_exito(request):

    return render(request, 'cuenta_activada_exito.html')