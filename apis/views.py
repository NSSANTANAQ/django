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
from rest_framework_simplejwt.tokens import BlacklistMixin, RefreshToken
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
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
            if TokenBlacklist.objects.filter(token=access_token).exists():
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



@method_decorator(csrf_exempt, name='dispatch')
class RegisterSubscriptionView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            endpoint = data.get('endpoint')
            keys = data.get('keys', {})
            p256dh = keys.get('p256dh')
            auth = keys.get('auth')

            if not all([endpoint, p256dh, auth]):
                return JsonResponse({'error': 'Faltan datos de suscripción.'}, status=400)

            subscription, created = Suscripcion.objects.get_or_create(
                endpoint=endpoint,
                defaults={
                    'p256dh': p256dh,
                    'auth_key': auth
                }
            )

            if not created:
                subscription.p256dh = p256dh
                subscription.auth_key = auth
                subscription.save()

            return JsonResponse({'success': True, 'message': 'Suscripción registrada exitosamente.'})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Formato de datos inválido.'}, status=400)
        except Exception as e:
            # Agregar log de error para diagnosticar problemas
            print(f"Error: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)


class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        # Agregar información personalizada a la respuesta si es necesario
        return response


class CustomTokenRefreshView(TokenRefreshView):
    permission_classes = [permissions.AllowAny]

class BlacklistTokenView(BlacklistMixin, APIView):
    def post(self, request, *args, **kwargs):
        token = request.data.get('token')

        if token:
            try:
                TokenBlacklist.objects.create(token=token)
                return Response({'message': 'Token revoked successfully.'}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'Token not provided.'}, status=status.HTTP_400_BAD_REQUEST)
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