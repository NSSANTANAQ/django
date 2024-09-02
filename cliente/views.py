from django.shortcuts import render
from .models import AdCliente, AdCuenta
from django.db import connections
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def menu_usuarios(request):
    return render(request, 'menu_usuarios.html')
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
            print(cliente_data['cliente_id'])
            # Consulta para obtener las cuentas relacionadas con el cliente
            cursor.execute('SELECT * FROM administracion.ad_cuenta WHERE cliente = %s AND estado = 24', [cliente_data['cliente_id']])
            cuentas_result = cursor.fetchall()
            print(cuentas_result)
    else:
        cuentas_result = []

    # Preparar los datos para el contexto de la plantilla
    context = {
        'cliente': cliente_data,  # Pasar el diccionario de datos del cliente
        'cuentas': cuentas_result,
    }

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
            'SELECT * FROM financiero.ren_liquidacion WHERE cuenta = %s AND tipo_liquidacion = 1 ORDER BY id DESC LIMIT 1',
            [cuenta_id]
        )
        cuentas_result = cursor.fetchall()

        # Consulta para obtener los convenios
        cursor.execute(
            'SELECT * FROM financiero.fn_solicitud_convenio WHERE cuenta = %s AND estado = 2',
            [cuenta_id]
        )
        convenio_result = cursor.fetchone()

    if cuentas_result:
        cuenta = cuentas_result[0]
        subtotal1 = cuenta[12]  # Campo 12 de la cuenta
        total_pagar = cuenta[4]  # Campo 4 de la cuenta
        interes = cuenta[13]  # Campo 13 de la cuenta
        subtotal =  subtotal1 + interes
        total = subtotal + total_pagar

        context = {
            'convenios': convenio_result,  # Agrega los convenios al contexto
            'cliente': cliente_data,
            'cuentas': cuentas_result,
            'cuenta': cuenta,
            'subtotal': subtotal,
            'total': total
        }

        return render(request, 'usuarios_consulta_cuentas_detalle.html', context)
    else:
        context = {
            'error': 'Cuenta no encontrada'
        }
        return render(request, 'usuarios_consulta_cuentas_detalle.html', context)