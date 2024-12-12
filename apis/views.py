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

@api_view(['GET'])
def login_view(request):
    username = request.query_params.get('username')  # Obtiene datos de la URL
    password = request.query_params.get('password')

    user = authenticate(username=username, password=password)

    if user is not None:
        return Response({
            'success': True,
            'message': 'Login exitoso'
        })
    else:
        return Response({
            'success': False,
            'message': 'Usuario o contraseña incorrectos'
        })