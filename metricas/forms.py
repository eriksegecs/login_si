from django import forms
from django.views.generic.list import ListView
from .models import Metrica, User, UserManager
from django.contrib.auth.forms import UserCreationForm,UsernameField
from django.contrib.auth.base_user import BaseUserManager
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import (
    make_password, identify_hasher,
)
User = get_user_model()

class MetricForm(forms.Form):
    METRICAS_CHOICES = [
    ('CPU', 'CPU'),
    ('Memória', 'Memória'),
    ('Disco', 'Disco'),
    ]

    VALOR_CHOICES = [
    (1, '0 a 25'),
    (2, '25 a 50'),
    (3, '50 a 75'),
    (4, '75 a 100'),
    ]
    
    valor = forms.CharField(
        max_length=200,
        widget=forms.Select(choices=VALOR_CHOICES),
        
    )
    nome = forms.MultipleChoiceField(
        label='Categoria',
        widget=forms.SelectMultiple,
        choices=METRICAS_CHOICES,
        required=False
        )

    def get_metricas(self, nome):
        return Metrica.objects.filter(nome=nome)


class MetricListView(ListView):
    model = Metrica
    paginate_by = 200   # if pagination is desired


class UserCreationFormEmail(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email")
        field_classes = {'username': UsernameField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs['autofocus'] = True
        

    def save(self, commit=True):
        user = super(UserCreationFormEmail, self).save(commit=False)
        user.is_staff = True
        if commit:
            user.save()
        return user


class UserResetPasswordForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ["email"]
