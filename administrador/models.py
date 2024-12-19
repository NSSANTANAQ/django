from django.db import models
from cloudinary.models import CloudinaryField

class Noticia(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    subtitulo = models.CharField(max_length=200)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

class ImagenNoticia(models.Model):
    noticia = models.ForeignKey(Noticia, related_name='imagenes', on_delete=models.CASCADE)
    imagen = CloudinaryField('imagen')


    def __str__(self):
        return f"Imagen de {self.noticia.titulo}"