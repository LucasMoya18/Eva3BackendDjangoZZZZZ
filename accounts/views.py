from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from .models import Ticket, Cliente
from .forms import TicketForm, CommentForm, UserRegistrationForm, ClientForm

@login_required
def tickets(request):
    tickets = Ticket.objects.all()
    return render(request, 'tickets/tickets.html', {'tickets': tickets})

@login_required
def ticket_detalle(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.ticket = ticket
            comment.author = request.user
            comment.save()
            return redirect('ticket_detalle', pk=pk)
    else:
        form = CommentForm()
    return render(request, 'tickets/ticket_detalle.html', {'ticket': ticket, 'form': form})

@login_required
def crearTicket(request):
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
def actTicket(request, pk):
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
def delTicket(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if request.method == 'POST':
        ticket.delete()
        return redirect('tickets')
    return render(request, 'tickets/ticket_eliminar.html', {'ticket': ticket})

@login_required
def dashboard(request):
    open_tickets = Ticket.objects.filter(status='OPEN').count()
    in_progress_tickets = Ticket.objects.filter(status='IN_PROGRESS').count()
    resolved_tickets = Ticket.objects.filter(status='RESOLVED').count()
    closed_tickets = Ticket.objects.filter(status='CLOSED').count()
    context = {
        'open_tickets': open_tickets,
        'en_progreso_tickets': in_progress_tickets,
        'resuelto_ticket': resolved_tickets,
        'cerrado_ticket': closed_tickets,
    }
    return render(request, 'tickets/dashboard.html', context)

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/registro.html', {'form': form})

@login_required
def registroCliente(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente registrado exitosamente.')
            return redirect('listaCliente')
    else:
        form = ClientForm()
    return render(request, 'registration/cliente_form.html', {'form': form})

@login_required
def listaCliente(request):
    clients = Cliente.objects.all()
    return render(request, 'clientes.html', {'clients': clients})
