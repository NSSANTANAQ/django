from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignUpForm,LoginForm, ConsultaClienteForm
from django.contrib import messages
from django.contrib.auth import logout
from cliente.models import AdCliente
from django.http import JsonResponse
from django.db import connections, OperationalError
from django.views.decorators.csrf import csrf_exempt

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            messages.error(request, 'Tu cuenta está desactivada.')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('menu_usuarios')  # Cambia 'home' por la URL a la que quieras redirigir al usuario después del login
                else:
                    messages.error(request, 'Tu cuenta está desactivada.')
            else:
                messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = LoginForm()

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
                return JsonResponse({'status': 'error', 'message': str(e)})
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
            form.save()
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