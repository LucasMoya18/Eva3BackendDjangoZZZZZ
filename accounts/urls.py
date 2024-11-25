from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('tickets/', views.tickets, name='tickets'),
    path('tickets/<int:pk>/', views.ticket_detalle, name='ticket_detalle'),
    path('tickets/nuevo/', views.crearTicket, name='crearTicket'),
    path('tickets/<int:pk>/editar/', views.actTicket, name='actTicket'),
    path('tickets/<int:pk>/eliminar/', views.delTicket, name='delTicket'),
    path('registro/', views.register, name='register'),
    path('clientes/', views.listaCliente, name='listaCliente'),
    path('clientes/registro/', views.registroCliente, name='registroCliente'),
]