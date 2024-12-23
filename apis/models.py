from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User


# Create your models here.
class Suscripcion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=512)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Suscripción {self.id}"
