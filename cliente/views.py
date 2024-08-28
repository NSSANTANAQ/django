from django.shortcuts import render
from .models import AdCliente, AdCuenta
from django.db import connections
# Create your views here.


def menu_usuarios(request):

    return render(request, 'menu_usuarios.html')
def usuarios_consulta_cuentas(request):
    cedula_ruc = request.user.username  # Supongo que cedula_ruc está en el nombre de usuario

    with connections['railway'].cursor() as cursor:
        # Consulta para obtener el cliente con el número de cédula
        cursor.execute('SELECT * FROM administracion.ad_cliente WHERE cedula_ruc = %s', [cedula_ruc])
        cliente_result = cursor.fetchone()

        if cliente_result:
            cliente_id = cliente_result[0]  # Asumiendo que el ID es el primer campo en el resultado

            # Consulta para obtener las cuentas relacionadas con el cliente
            cursor.execute('SELECT * FROM administracion.ad_cuenta WHERE cliente = %s AND estado = 24', [cliente_id])
            cuentas_result = cursor.fetchall()
        else:
            cuentas_result = []



    # Preparar los datos para el contexto de la plantilla
    context = {
        'cliente': cliente_result,
        'cuentas': cuentas_result,

    }

    return render(request, 'usuarios_consulta_cuentas.html', context)


def usuarios_consulta_cuentas_detalle(request, cuenta_id):
    cedula_ruc = request.user.username  # Supongo que cedula_ruc está en el nombre de usuario

    with connections['railway'].cursor() as cursor:
        # Consulta para obtener el cliente con el número de cédula
        cursor.execute('SELECT * FROM administracion.ad_cliente WHERE cedula_ruc = %s', [cedula_ruc])
        cliente_result = cursor.fetchone()

        cuentas_result = []
        total = None
        cuenta = None

        if cliente_result:
            # Consulta para obtener la última liquidación relacionada con la cuenta
            cursor.execute('SELECT * FROM financiero.ren_liquidacion WHERE cuenta = %s ORDER BY id DESC LIMIT 1', [cuenta_id])
            cuentas_result = cursor.fetchall()

            if cuentas_result:
                cuenta = cuentas_result[0]  # La última liquidación encontrada

                # Suponiendo que `subtotal` está en el índice 12 y `interes` en el índice 13
                subtotal = cuenta[12]
                interes = cuenta[13]
                total = subtotal + interes  # Suma de subtotal e interés

    # Preparar los datos para el contexto de la plantilla
    context = {
        'cliente': cliente_result,
        'cuentas': cuentas_result,
        'cuenta': cuenta,
        'total': total
    }

    return render(request, 'usuarios_consulta_cuentas_detalle.html', context)