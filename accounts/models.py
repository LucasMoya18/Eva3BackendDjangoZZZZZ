from django.db import models
from django.contrib.auth.models import User

class Cliente(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.name

class Ticket(models.Model):
    STATUS_CHOICES = [
        ('OPEN', 'Abierto'),
        ('IN_PROGRESS', 'En Proceso'),
        ('RESOLVED', 'Resuelto'),
        ('CLOSED', 'Cerrado'),
    ]
    PRIORITY_CHOICES = [
        ('LOW', 'Baja'),
        ('MEDIUM', 'Media'),
        ('HIGH', 'Alta'),
    ]
    title = models.CharField(max_length=200, verbose_name='Problema:')
    description = models.TextField(verbose_name='Descripcion:')
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='Creado en:')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPEN', verbose_name='Estado:')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='MEDIUM')
    Cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True , verbose_name='Asignado a:')

    def __str__(self):
        return f"{self.title} - {self.get_status_display()}"

class Comment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(verbose_name='Comentario:')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creado en:')

    def __str__(self):
        return f"Comentado por {self.author.username} en {self.ticket.title}"


