from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('tickets/', views.tickets, name='tickets'),
    path('tickets/<int:pk>/', views.ticket_detalle, name='ticket_detalle'),
    path('tickets/nuevo/', views.crear_ticket, name='crear_ticket'),
    path('tickets/<int:pk>/editar/', views.actualizar_ticket, name='actualizar_ticket'),
    path('tickets/<int:pk>/eliminar/', views.eliminar_ticket, name='eliminar_ticket'),
    path('registro/', views.registro_usuario, name='registro_usuario'),
    path('clientes/', views.lista_clientes, name='lista_clientes'),
    path('clientes/registro/', views.registro_cliente, name='registro_cliente'),
]