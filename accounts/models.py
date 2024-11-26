from django.db import models
from django.contrib.auth.models import User

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()

    def __str__(self):
        return self.nombre
    


class Ticket(models.Model):
    OPCIONES_ESTADO = [
        ('ABIERTO', 'Abierto'),
        ('EN_PROCESO', 'En Proceso'),
        ('RESUELTO', 'Resuelto'),
        ('CERRADO', 'Cerrado'),
    ]
    OPCIONES_PRIORIDAD = [
        ('BAJA', 'Baja'),
        ('MEDIA', 'Media'),
        ('ALTA', 'Alta'),
    ]
    titulo = models.CharField(max_length=200, verbose_name='Problema:')
    descripcion = models.TextField(default='',verbose_name='Descripción:')
    creado_en = models.DateTimeField(auto_now_add=True, verbose_name='Creado en:')
    estado = models.CharField(max_length=20, choices=OPCIONES_ESTADO, default='ABIERTO', verbose_name='Estado:')
    prioridad = models.CharField(max_length=10, choices=OPCIONES_PRIORIDAD, default='MEDIA', verbose_name='Prioridad:')
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    asignado_a = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Asignado a:')

class Comentario(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='comentarios')
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField(verbose_name='Comentario:')
    creado_en = models.DateTimeField(auto_now_add=True, verbose_name='Creado en:')

    def __str__(self):
        return f"Comentado por {self.autor.username} en {self.ticket.titulo}"


