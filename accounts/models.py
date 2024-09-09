from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta


class ActivationCode(models.Model):
    username = models.CharField(max_length=255)  # La cédula del usuario (también el username en auth_user)
    email = models.EmailField()
    code = models.CharField(max_length=50, unique=True)  # Código de activación
    expiration_time = models.DateTimeField()

    def is_expired(self):
        return timezone.now() > self.expiration_time

    def save(self, *args, **kwargs):
        if not self.expiration_time:
            self.expiration_time = timezone.now() + timedelta(minutes=10)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Activation code for {self.username}"
