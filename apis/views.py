from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Suscripcion
from .serializer import UserSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view

class UserListCreateAPIView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

@api_view(['POST'])
def login_view(request):
    if request.method == 'POST':
        # Obtener las credenciales enviadas
        username = request.data.get('username')
        password = request.data.get('password')

        # Validar las credenciales
        user = authenticate(username=username, password=password)

        if user is not None:
            return Response({
                'success': True,
                'message': 'Login exitoso',

            })
        else:
            return Response({
                'success': False,
                'message': 'Usuario o contraseña incorrectos'
            }, status=401)
    else:
        return Response({
            'success': False,
            'message': 'Método no permitido'
        }, status=405)

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