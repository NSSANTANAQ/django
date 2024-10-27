from decimal import Decimal, ROUND_UP
from .models import AdCliente, AdCuenta
from django.db import connections
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout

@login_required(login_url='login')
def menu_usuarios(request):
    return render(request, 'menu_usuarios.html')

@login_required(login_url='login')
def usuarios_perfil(request):
    cedula_ruc = request.user.username  # Asumiendo que cedula_ruc está en el nombre de usuario

    # Verificar si los datos del cliente ya están almacenados en la sesión

    with connections['railway'].cursor() as cursor:
        # Consulta para obtener el cliente con el número de cédula
        cursor.execute('SELECT * FROM administracion.ad_cliente WHERE cedula_ruc = %s', [cedula_ruc])
        cliente_result = cursor.fetchone()

        if cliente_result:
            # Guardar los datos del cliente en la sesión
            contexto = {
                'cliente_id': cliente_result[0],
                'cedula': cliente_result[1],  # Asumiendo que el ID es el primer campo
                'nombre': cliente_result[2],  # Y el nombre en la segunda posición, etc.
                'direccion': cliente_result[4],
                'correo': cliente_result[10],
                'celular': cliente_result[11],
                # Añadir más campos según la estructura de tu tabla
            }
        else:
            # Si no se encuentra el cliente, se puede manejar el caso
            request.session['cliente_data'] = None
    messages.success(request, 'Exito')
    return render(request, 'usuarios_perfil.html', contexto)

@login_required(login_url='login')
def usuarios_consulta_cuentas(request):
    cedula_ruc = request.user.username  # Asumiendo que cedula_ruc está en el nombre de usuario

    # Verificar si los datos del cliente ya están almacenados en la sesión
    if 'cliente_data' not in request.session:
        with connections['railway'].cursor() as cursor:
            # Consulta para obtener el cliente con el número de cédula
            cursor.execute('SELECT * FROM administracion.ad_cliente WHERE cedula_ruc = %s', [cedula_ruc])
            cliente_result = cursor.fetchone()

            if cliente_result:
                # Guardar los datos del cliente en la sesión
                request.session['cliente_data'] = {
                    'cliente_id': cliente_result[0],
                    'cedula': cliente_result[1],  # Asumiendo que el ID es el primer campo
                    'nombre': cliente_result[2],      # Y el nombre en la segunda posición, etc.
                    'direccion': cliente_result[4],
                    # Añadir más campos según la estructura de tu tabla
                }
            else:
                # Si no se encuentra el cliente, se puede manejar el caso
                request.session['cliente_data'] = None

    # Recuperar los datos del cliente desde la sesión
    cliente_data = request.session.get('cliente_data')

    # Si el cliente fue encontrado, se procede a buscar las cuentas
    if cliente_data:
        with connections['railway'].cursor() as cursor:
            # Consulta para obtener las cuentas relacionadas con el cliente
            cursor.execute('SELECT * FROM administracion.ad_cuenta WHERE cliente = %s AND estado = 24', [cliente_data['cliente_id']])
            cuentas_result = cursor.fetchall()

    else:
        cuentas_result = []

    # Preparar los datos para el contexto de la plantilla
    context = {
        'cliente': cliente_data,  # Pasar el diccionario de datos del cliente
        'cuentas': cuentas_result,
    }
    messages.success(request, 'Exito')
    return render(request, 'usuarios_consulta_cuentas.html', context)

@login_required(login_url='login')
def usuarios_consulta_cuentas_detalle(request, cuenta_id):
    cedula_ruc = request.user.username  # Asumiendo que cedula_ruc está en el nombre de usuario

    # Verificar si los datos del cliente ya están almacenados en la sesión
    if 'cliente_data' not in request.session:
        with connections['railway'].cursor() as cursor:
            # Consulta para obtener el cliente con el número de cédula
            cursor.execute('SELECT * FROM administracion.ad_cliente WHERE cedula_ruc = %s', [cedula_ruc])
            cliente_result = cursor.fetchone()

            if cliente_result:
                # Guardar los datos del cliente en la sesión
                request.session['cliente_data'] = {
                    'cliente_id': cliente_result[0],
                    'cedula': cliente_result[1],  # Asumiendo que el ID es el primer campo
                    'nombre': cliente_result[2],  # Y el nombre en la segunda posición, etc.
                    'direccion': cliente_result[4],
                    # Añadir más campos según la estructura de tu tabla
                }
            else:
                # Si no se encuentra el cliente, se puede manejar el caso
                request.session['cliente_data'] = None

    # Recuperar los datos del cliente desde la sesión
    cliente_data = request.session.get('cliente_data')

    with connections['railway'].cursor() as cursor:
        # Consulta para obtener la cuenta

        cursor.execute(
            '''
            SELECT COUNT(*), SUM(saldo) 
            FROM financiero.ren_liquidacion 
            WHERE cuenta = %s AND tipo_liquidacion = 1 AND estado_liquidacion = 2 
            AND id != (
                SELECT MAX(id) 
                FROM financiero.ren_liquidacion 
                WHERE cuenta = %s AND tipo_liquidacion = 1 AND estado_liquidacion = 2
            )
            ''',
            [cuenta_id, cuenta_id]
        )
        result = cursor.fetchone()

        cuenta_total = result[0] + 1  # COUNT(*)
        saldo_total = result[1]  # SUM(saldo)

        cursor.execute(
            'SELECT * FROM financiero.ren_liquidacion WHERE cuenta = %s AND tipo_liquidacion = 1 AND estado_liquidacion = 2 ORDER BY id DESC LIMIT 1',
            [cuenta_id]
        )

        cuentas_result = cursor.fetchall()
        datos_cuenta = cuentas_result[0]
        mes = datos_cuenta[2]

        cursor.execute(
            'SELECT * FROM financiero.ren_mes_facturacion WHERE id = %s',
            [mes]
        )
        mes_facturacion_result = cursor.fetchall()

        # Consulta para obtener los convenios
        cursor.execute(
            'SELECT * FROM financiero.fn_solicitud_convenio WHERE cuenta = %s AND estado = 2',
            [cuenta_id]
        )
        convenio_result = cursor.fetchone()


    if cuentas_result:

        mes_facturacion = mes_facturacion_result[0]
        cuenta = cuentas_result[0]
        total_pagar = cuenta[4]
        cuenta_total_int = int(cuenta_total)

        cuenta_total_int = cuenta_total_int if cuenta_total_int is not None else Decimal(0)
        saldo_total = saldo_total if saldo_total is not None else Decimal(0)

        interes_num = Decimal('0.0054') * Decimal(cuenta_total_int) * Decimal(saldo_total)
        interes = interes_num.quantize(Decimal('0.01'), rounding=ROUND_UP)
        subtotal = saldo_total + interes
        total = subtotal + total_pagar

        context = {
            'mes_facturacion': mes_facturacion,  # Agrega los convenios al contexto
            'convenios': convenio_result,  # Agrega los convenios al contexto
            'cliente': cliente_data,
            'cuentas': cuentas_result,
            'cuenta': cuenta,
            'subtotal': subtotal,
            'total': total,
            'cuenta_total': cuenta_total,
            'saldo_total': saldo_total,
            'interes': interes
        }

        return render(request, 'usuarios_consulta_cuentas_detalle.html', context)
    else:
        context = {
            'error': 'Cuenta no encontrada'
        }
        return render(request, 'usuarios_consulta_cuentas_detalle.html', context)
@login_required(login_url='login')
def usuarios_noticias(request):
    messages.success(request, 'Exito')
    return render(request, 'usuarios_noticias.html')
@login_required(login_url='login')
def usuarios_cambiar_password(request):
    user = request.user

    if request.method == 'POST':

        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            # Redirige a una página de confirmación o muestra un mensaje de éxito
            messages.success(request,'Cambio de Contraseña Exitoso, vuelve a iniciar sesion con tu nueva contraseña')
            return redirect('usuarios_cambiar_password_exito')
    else:
        form = SetPasswordForm(user)
        messages.success(request, 'Exito')
    return render(request, 'usuarios_cambiar_password.html', {'form': form})

def usuarios_cambiar_password_exito(request):
    logout(request)
    messages.success(request, 'Contraseña cambiada con Exito')
    return render(request, 'usuarios_cambiar_password_exito.html')