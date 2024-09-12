from django.shortcuts import render, redirect
from .forms import ReservationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Reservation
from django.core.paginator import Paginator

def reservation_view(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('reservation_success')  # Redirection après soumission
    else:
        form = ReservationForm()

    return render(request, 'reservation/reservation_form.html', {'form': form})

def admin_login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('clients')  # Redirection vers la page des clients
        else:
            messages.error(request, 'Identifiants invalides.')
    
    return render(request, 'reservation/admin_login.html')


@login_required  # Limite l'accès aux utilisateurs authentifiés
def clients_list_view(request):
   # reservations = Reservation.objects.all()
   # return render(request, 'reservation/clients_list.html', {'reservations': reservations})
    query_nom = request.GET.get('nom')  # Rechercher par nom
    query_date = request.GET.get('date')  # Rechercher par date

    # Filtrer les résultats
    reservations = Reservation.objects.all()

    if query_nom:
        reservations = reservations.filter(nom__icontains=query_nom)  # Recherche insensible à la casse

    if query_date:
        reservations = reservations.filter(date_reservation=query_date)

    # Pagination
    paginator = Paginator(reservations, 5)  # 5 réservations par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'reservation/clients_list.html', {
        'reservations': reservations,
        'page_obj': page_obj,
        'paginator':paginator,
        'page_number':page_number,
        'query_nom': query_nom,
        'query_date': query_date,
    })
