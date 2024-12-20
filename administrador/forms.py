from django import forms
from .models import Noticia, ImagenNoticia
from django.forms import modelformset_factory
class NoticiaForm(forms.ModelForm):
    class Meta:
        model = Noticia
        fields = ['titulo', 'subtitulo', 'contenido']

class ImagenNoticiaForm(forms.ModelForm):
    imagen = forms.ImageField(required=True)  # Campo para subir imágenes

    class Meta:
        model = ImagenNoticia
        fields = ['imagen']