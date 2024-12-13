from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Suscripcion, TokenBlacklist
from .serializer import UserSerializer
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
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

class UserListCreateAPIView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

@api_view(['POST'])
class LoginApiView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)


class ProtectedView(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        return Response({'message': 'Acceso permitido'}, status=status.HTTP_200_OK)



class RegistrarSuscripcionView(APIView):
    def post(self, request):
        # Obtener datos de la suscripción desde la solicitud
        data = request.data
        endpoint = data.get('endpoint')
        p256dh = data.get('keys', {}).get('p256dh')
        auth = data.get('keys', {}).get('auth')

        # Verificar que no exista ya esta suscripción
        if not Suscripcion.objects.filter(endpoint=endpoint).exists():
            # Registrar la suscripción
            Suscripcion.objects.create(endpoint=endpoint, p256dh=p256dh, auth=auth)
            return Response({'message': 'Suscripción registrada exitosamente'}, status=status.HTTP_201_CREATED)
        return Response({'message': 'La suscripción ya existe'}, status=status.HTTP_200_OK)


class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        # Agregar información personalizada a la respuesta si es necesario
        return response


class CustomTokenRefreshView(TokenRefreshView):
    permission_classes = [permissions.AllowAny]


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def revoke_token_view(request):
    user = request.user
    token = request.data.get('token')

    if token:
        try:
            TokenBlacklist.objects.create(user=user, token=token)
            return Response({"msg": "Token revoked successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"error": "Token not provided"}, status=status.HTTP_400_BAD_REQUEST)