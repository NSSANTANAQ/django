from rest_framework import serializers
from django.contrib.auth.models import User
from cliente.models import AdCuenta , RenLiquidacion


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'password']


class CuentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdCuenta
        fields = ['id', 'zona', 'sector', 'mz', 'direccion', 'nombre_calle', 'cliente', 'estado']

class DetalleFinancieroSerializer(serializers.ModelSerializer):
    class Meta:
        model =RenLiquidacion
        fields = ['mes_facturacion', 'saldo', 'estado_liquidacion']