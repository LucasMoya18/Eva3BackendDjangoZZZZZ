from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from .models import Ticket, Cliente
from .forms import TicketForm, ComentarioForm, RegistroUsuarioForm, ClienteForm

@login_required
def tickets(request):
    estado = request.GET.get('estado')
    prioridad = request.GET.get('prioridad')
    tecnico = request.GET.get('tecnico')


    tickets = Ticket.objects.all()
    if estado:
        tickets = tickets.filter(estado=estado)
    if prioridad:
        tickets = tickets.filter(prioridad=prioridad)
    if tecnico:
        tickets = tickets.filter(asignado_a_id=tecnico)

    tecnicos = User.objects.all() 
    return render(request,'tickets/tickets.html',{'tickets': tickets, 'estados': Ticket.OPCIONES_ESTADO, 'prioridades': Ticket.OPCIONES_PRIORIDAD, 'tecnicos': tecnicos}
)

@login_required
def ticket_detalle(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.ticket = ticket
            comentario.autor = request.user
            comentario.save()
            return redirect('ticket_detalle', pk=pk)
    else:
        form = ComentarioForm()
    return render(request, 'tickets/ticket_detalle.html', {'ticket': ticket, 'form': form})

@login_required
def crear_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.save()
            return redirect('ticket_detalle', pk=ticket.pk)
    else:
        form = TicketForm()
    return render(request, 'tickets/ticket_formulario.html', {'form': form})

@login_required
def actualizar_ticket(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if request.method == 'POST':
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            ticket = form.save()
            return redirect('ticket_detalle', pk=ticket.pk)
    else:
        form = TicketForm(instance=ticket)
    return render(request, 'tickets/ticket_formulario.html', {'form': form})

@login_required
def eliminar_ticket(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if request.method == 'POST':
        ticket.delete()
        return redirect('tickets')
    return render(request, 'tickets/ticket_eliminar.html', {'ticket': ticket})

@login_required
def dashboard(request):
    abiertos = Ticket.objects.filter(estado='ABIERTO').count()
    en_proceso = Ticket.objects.filter(estado='EN_PROCESO').count()
    resueltos = Ticket.objects.filter(estado='RESUELTO').count()
    cerrados = Ticket.objects.filter(estado='CERRADO').count()
    context = {
        'abiertos': abiertos,
        'en_proceso': en_proceso,
        'resueltos': resueltos,
        'cerrados': cerrados,
    }
    return render(request, 'tickets/dashboard.html', context)

def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            return redirect('dashboard')
    else:
        form = RegistroUsuarioForm()
    return render(request, 'registration/registro.html', {'form': form})

@login_required
def registro_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente registrado exitosamente.')
            return redirect('lista_clientes')
    else:
        form = ClienteForm()
    return render(request, 'registration/cliente_form.html', {'form': form})

@login_required
def lista_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'clientes.html', {'clientes': clientes})
