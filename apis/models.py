from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User

class TokenBlacklist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=512)
    created_at = models.DateTimeField(auto_now_add=True)

    def revoke_token(self):
        self.token_blacklist.add(self)
# Create your models here.
class Suscripcion(models.Model):
    endpoint = models.TextField()  # URL del cliente para recibir notificaciones
    p256dh = models.TextField()    # Clave pública del cliente
    auth = models.TextField()      # Token de autenticación del cliente

    def __str__(self):
        return f"Suscripción {self.id}"
