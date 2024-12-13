from django.urls import path
from . import views
from .views import revoke_token_view, UserListCreateAPIView,LoginApiView,RegistrarSuscripcionView,CustomTokenObtainPairView,CustomTokenRefreshView

urlpatterns = [
    # Define tus endpoints aquí
    path('users/', UserListCreateAPIView.as_view(), name='user-list-create'),
    path('login_api/', LoginApiView.as_view(), name='login_api'),
    path('registrar-suscripcion/', RegistrarSuscripcionView.as_view(), name='registrar_suscripcion'),

    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('revoke-token/', revoke_token_view, name='revoke_token'),
]