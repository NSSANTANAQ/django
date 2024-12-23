from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from cliente.models import AdCliente
from django.core.exceptions import ValidationError
import re


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'autocomplete': 'username',
            'placeholder': 'Cedula de Identidad',
            'class': 'form-control',
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'current-password',
            'placeholder': 'Contraseña',
            'class': 'form-control',
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("Usuario o contraseña incorrectos.")
            elif not user.is_active:
                raise forms.ValidationError("Esta cuenta está desactivada.")

        return cleaned_data


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'autocomplete': 'username',
            'placeholder': 'Cedula de Identidad',
            'class': 'form-control',
        })
    )
    email = forms.EmailField(widget=forms.PasswordInput(attrs={
            'autocomplete': 'email',
            'placeholder': 'Correo Electronico',
            'class': 'form-control',
        }))
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'current-password',
            'placeholder': 'Contraseña',
            'class': 'form-control',
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'current-password',
            'placeholder': 'Contraseña',
            'class': 'form-control',
        })
    )
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class ConsultaClienteForm(forms.ModelForm):
    class Meta:
        model = AdCliente
        fields = ['cedula_ruc']


