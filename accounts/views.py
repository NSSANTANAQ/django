from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.encoding import force_bytes
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
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage, BadHeaderError
from rest_framework.response import Response
from rest_framework.decorators import api_view


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = form.data.get('username')  # Obtenemos el username del formulario
        password = form.data.get('password')  # Obtenemos el password del formulario

        try:
            # Intentamos obtener el usuario por el username
            user = User.objects.get(username=username)

            # Verificamos si el usuario está activo
            if not user.is_active:
                return redirect('activar_cuenta_modal', user.pk)

            # Validamos el formulario
            if form.is_valid():
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, f'Bienvenido!, {request.user.username}')

                    # Redireccionamos según el tipo de usuario
                    if user.is_staff:  # Usuario admin
                        return redirect('menu_admin')  # Nombre de la URL del admin
                    else:  # Usuario regular
                        return redirect('menu_usuarios')  # Nombre de la URL del cliente
                else:
                    messages.error(request, 'Usuario o contraseña incorrectos.')
            else:
                messages.error(request, 'Activa tu cuenta con el código de activación.')

        except User.DoesNotExist:  # Capturamos el error si el usuario no existe
            messages.error(request, 'Usuario no registrado.')

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

            resultado_envio = send_activation_email(user)

            if resultado_envio == 1:
                return JsonResponse({'status': 'success', 'message': 'Usuario registrado exitosamente.'})
            else:
                return JsonResponse({'status': 'success', 'message': 'Error del servicio intentelo mas tarde'})

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
            print('Error en el servicio, por favor intente de nuevo más tarde.')
            # Maneja los errores relacionados con encabezados inválidos
            return 0
        except Exception as e:
            print('Error en el servicio, por favor intente de nuevo más tarde.')
            # Maneja otros errores relacionados con el envío de correos
            return 0

        # Si todo sale bien, puedes retornar un mensaje de éxito o redirigir al usuario
        print('Código de activación enviado con éxito.')
        return 1

    except Exception as e:
        # Maneja cualquier otro error en la función
        return 0


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

def password_reset_request(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data['email']
            associated_users = User.objects.filter(email=data)
            if associated_users.exists():
                for user in associated_users:
                    subject = "Cambio de contraseña solicitado"
                    html_email_template_name = "password_reset_email.html"
                    c = {
                        "email": user.email,
                        'domain': 'serviciosenlinea.epmapas.gob.ec',
                        'site_name': 'Recuperar Contraseña',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email_html_content = render_to_string(html_email_template_name, c)
                    email = EmailMessage(
                        subject=subject,
                        body=email_html_content,
                        from_email='serviciosenlinea@epmapas.gob.ec',
                        to=[user.email],
                    )
                    email.content_subtype = "html"  # Esto asegura que el correo se envíe como HTML

                    try:
                        email.send(fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')

                    messages.success(request, 'El enlace para restablecer la contraseña ha sido enviado a tu correo electrónico.')
                    return redirect('envio_exitoso_enlace_email')
            else:
                messages.error(request, 'No existe una cuenta asociada a ese correo electrónico.')
                return render(request=request, template_name="recuperar_password.html", context={"form": form})

    form = PasswordResetForm()
    return render(request=request, template_name="recuperar_password.html", context={"form": form})


def envio_exitoso_enlace_email(request):
    return render(request, 'envio_exitoso_enlace_email.html')

def my_password_reset_confirm(request, uidb64, token):
        UserModel = get_user_model()
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = UserModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            if request.method == 'POST':
                form = SetPasswordForm(user, request.POST)
                if form.is_valid():
                    form.save()
                    # Redirige a una página de confirmación o muestra un mensaje de éxito
                    return redirect('password_reset_exito')
            else:
                form = SetPasswordForm(user)
            return render(request, 'password_reset_confirm.html', {'form': form})
        else:
            # Redirige a una página de error o muestra un mensaje de error
            return render(request, 'invalid_token.html')

def password_reset_exito(request):
    return render(request,'password_reset_exito.html')


@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        return Response({"message": "Inicio de sesión exitoso", "status": "success"})
    else:
        return Response({"message": "Usuario o contraseña incorrectos", "status": "error"})