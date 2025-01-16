import os

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from firebase_admin import messaging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from firebase_admin import messaging, _http_client

from administrador.models import ImagenNoticia, Noticia
from cliente.models import AdCliente, AdCuenta
from .models import Suscripcion
from .serializer import UserSerializer, CuentaSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from django.http import JsonResponse
import base64
import json
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.tokens import BlacklistMixin, RefreshToken
import requests

class UserListCreateAPIView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

@api_view(['POST'])
class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            # Check if token is blacklisted
            if Suscripcion.objects.filter(token=access_token).exists():
                return Response({'message': 'Token revoked or expired'}, status=status.HTTP_401_UNAUTHORIZED)

            return Response({
                'token': access_token,
                'refresh': str(refresh),
            }, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class ProtectedView(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        return Response({'message': 'Acceso permitido'}, status=status.HTTP_200_OK)



@csrf_exempt
@api_view(['POST'])
def RegistrarSuscripcion(request):
    data = request.data
    endpoint = data.get('endpoint')
    p256dh = data.get('keys', {}).get('p256dh')
    auth = data.get('keys', {}).get('auth')

    # Verificar que no exista ya esta suscripción
    if not Suscripcion.objects.filter(endpoint=endpoint).exists():
        Suscripcion.objects.create(endpoint=endpoint, p256dh=p256dh, auth=auth)
        return Response({'message': 'Suscripción registrada exitosamente'}, status=status.HTTP_201_CREATED)
    return Response({'message': 'La suscripción ya existe'}, status=status.HTTP_200_OK)


# class CustomTokenObtainPairView(TokenObtainPairView):
#     permission_classes = [permissions.AllowAny]
#
#     def post(self, request, *args, **kwargs):
#         response = super().post(request, *args, **kwargs)
#         # Agregar información personalizada a la respuesta si es necesario
#         return response

class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:  # Solo registrar si la autenticación fue exitosa
            user = self.get_user(request)
            device_token = request.data.get('device_token')  # El token del dispositivo debe enviarse en la solicitud

            if device_token:
                # Registrar el token en el modelo Suscripcion
                Suscripcion.objects.create(user=user, token=device_token)

        return response

    def get_user(self, request):
        """
        Obtiene el usuario autenticado basado en las credenciales del request.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return serializer.user


class CustomTokenRefreshView(TokenRefreshView):
    permission_classes = [permissions.AllowAny]



@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Requiere autenticación
def register_token(request):
    token = request.data.get('token')  # Usar JSON para obtener el token

    if not token:
        return JsonResponse({'success': False, 'message': 'Token missing'}, status=400)

    # Obtener el usuario autenticado
    user = request.user

    # Crear o actualizar el token asociado al usuario
    Suscripcion.objects.update_or_create(token=token, defaults={'user': user})

    return JsonResponse({'success': True, 'message': 'Token registered'}, status=200)




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def revoke_token_view(request):
    user = request.user
    token = request.data.get('token')

    if token:
        try:
            Suscripcion.objects.create(user=user, token=token)
            return Response({"msg": "Token revoked successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"error": "Token not provided"}, status=status.HTTP_400_BAD_REQUEST)


def api_noticias(request):
    noticias = Noticia.objects.all()
    data = []

    for noticia in noticias:
        imagenes = ImagenNoticia.objects.filter(noticia=noticia)  # Obtener imágenes relacionadas
        imagen_urls = [imagen.imagen.url for imagen in imagenes]  # Extraer URLs

        data.append({
            "id": noticia.id,
            "titulo": noticia.titulo,
            "contenido": noticia.contenido,
            "subtitulo": noticia.subtitulo,
            "fecha_publicacion": noticia.fecha_publicacion,
            "imagenes": imagen_urls,  # Lista de URLs
        })

    return JsonResponse({"noticias": data})

class CuentasActivasView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # Obtener el número de cédula del usuario autenticado
        cedula_usuario = request.user.username # Supongo que el username es el número de cédula
        print(cedula_usuario)
        try:
            # Buscar al cliente con la cédula
            cliente = AdCliente.objects.using('railway').filter(cedula_ruc=cedula_usuario)
            cuentas_activas = AdCuenta.objects.using('railway').filter(cliente=cliente.id, estado=24)

            # Serializar las cuentas
            serializer = CuentaSerializer(cuentas_activas, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except AdCliente.DoesNotExist:
            return Response(
                {"error": "Cliente no encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )


