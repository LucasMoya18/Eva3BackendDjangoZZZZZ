from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Ticket, Comentario, Cliente

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['titulo', 'descripcion', 'prioridad', 'cliente', 'estado', 'asignado_a']

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['contenido']

class RegistroUsuarioForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        usuario = super(RegistroUsuarioForm, self).save(commit=False)
        usuario.email = self.cleaned_data['email']
        if commit:
            usuario.save()
        return usuario

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'correo']
