from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
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