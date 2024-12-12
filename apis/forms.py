from django import forms
from .models import PushSubscription

class PushSubscriptionForm(forms.ModelForm):
    class Meta:
        model = PushSubscription
        fields = ['endpoint', 'public_key', 'auth_key']