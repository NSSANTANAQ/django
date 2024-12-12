from django.db import models

# Create your models here.
class Suscripcion(models.Model):
    endpoint = models.TextField()  # URL del cliente para recibir notificaciones
    p256dh = models.TextField()    # Clave pública del cliente
    auth = models.TextField()      # Token de autenticación del cliente

    def __str__(self):
        return f"Suscripción {self.id}"