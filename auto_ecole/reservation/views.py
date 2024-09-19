from .forms import ReservationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Reservation
from django.core.paginator import Paginator
import requests
import uuid
from django.shortcuts import render, redirect,get_object_or_404
from django.conf import settings
from .forms import PaymentForm
from .models import Transaction
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render
from .models import Inscription
from datetime import date
from django.utils import timezone


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
        'page_obj': page_obj,
        'paginator':paginator,
        'page_number':page_number,
        'query_nom': query_nom,
        'query_date': query_date,
    })


def payment_view(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.identifier = str(uuid.uuid4())  # Générer un identifiant unique
            transaction.save()

            # Paramètres requis pour l'API PayGateGlobal
            payload = {
                "auth_token": settings.PAYGATE_API_TOKEN,
                "phone_number": transaction.phone_number,
                "amount": str(transaction.amount),
                "description": transaction.description,
                "identifier": transaction.identifier,
                "network": transaction.network,
            }

            # URL de l'API PayGateGlobal
            url = "https://paygateglobal.com/api/v1/pay"

            try:
                response = requests.post(url, json=payload)
                data = response.json()

                if data.get('status') == "0":
                    # Transaction initiée avec succès
                    transaction.tx_reference = data.get('tx_reference')
                    transaction.status = "Transaction enregistrée"
                    transaction.save()
                    return redirect('payment_success', transaction_id=transaction.id)
                else:
                    # Gérer les erreurs de transaction
                    transaction.status = "Erreur lors de l'enregistrement"
                    transaction.save()
                    return redirect('payment_failed')

            except Exception as e:
                # Gérer les exceptions
                print(f"Erreur: {e}")
                return redirect('payment_failed')
    else:
        form = PaymentForm()

    return render(request, 'reservation/payment_form.html', {'form': form})


def payment_success(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    return render(request, 'reservation/payment_success.html', {'transaction': transaction})

def payment_failed(request):
    return render(request, 'reservation/payment_failed.html')

def aceuill(request):

    return render(request,"reservation/index.html")


#sending mail

def contact_view(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        prenoms = request.POST.get('nom')
        message = request.POST.get('message')
        from_email = request.POST.get('email')
        
        send_mail(
            nom,
            prenoms,
            message,
            from_email,
            [settings.DEFAULT_FROM_EMAIL],
            fail_silently=False,
        )
        return render(request, 'contact_success.html')
    return render(request, 'contact.html')


def inscription(request):
    if request.method == "POST":
        # Récupérer les données postées
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenoms')
        email = request.POST.get('email')
        telephone = request.POST.get('telephone')
        ville = request.POST.get('ville')
        categorie = request.POST.get('categorie')
        formation = request.POST.get('formation')
        typecours = request.POST.get('typecours')
        avance = request.POST.get('avance')
        createAt=date.today()


        
        # Créer une instance du modèle Inscription avec les données récupérées
        new_inscription = Inscription(
            nom=nom,
            prenom=prenom,
            email=email,
            telephone=telephone,
            ville=ville,
            categorie=categorie,
            formation=formation,
            typecours=typecours,
            avance=avance,
            date=createAt,
        )
        
        # Sauvegarder dans la base de données
        new_inscription.save()
        if avance=="oui":
            return redirect('payment')
        
        # Rediriger après la soumission
        return render(request,"reservation/success_inscription.html") # Remplace 'success_page' par la route vers la page de succès.
    
    # Si la méthode n'est pas POST, on affiche simplement le formulaire
    return render(request, "reservation/inscription_test.html")

def dashboard(request):

    return render(request,"reservation/dashboard.html")


@login_required  # Limite l'accès aux utilisateurs authentifiés
def inscription_list_view(request):
   # reservations = Reservation.objects.all()
   # return render(request, 'reservation/clients_list.html', {'reservations': reservations})
    query_nom = request.GET.get('nom')  # Rechercher par nom
    query_date = request.GET.get('date')

    # Filtrer les résultats
    inscriptions = Inscription.objects.all().order_by('date')

    if query_nom:
        inscriptions = inscriptions.filter(nom__icontains=query_nom)  # Recherche insensible à la casse

    if query_date:
        inscriptions = inscriptions.filter(date=query_date)

    # Pagination
    paginator = Paginator(inscriptions, 6)  # 5 réservations par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'reservation/inscription_list.html', {
        'page_obj': page_obj,
        'paginator':paginator,
        'page_number':page_number,
        'query_nom': query_nom,
        'query_date': query_date,
    })



@login_required  # Limite l'accès aux utilisateurs authentifiés
def avance_list_view(request):
   # reservations = Reservation.objects.all()
   # return render(request, 'reservation/clients_list.html', {'reservations': reservations})
    query_nom = request.GET.get('nom')  # Rechercher par nom
    query_date = request.GET.get('date')  # Rechercher par date

    # Filtrer les résultats
    inscriptions = Inscription.objects.all().filter(Inscription.avance=="oui" and Transaction.status is not None)

    if query_nom:
        inscriptions = inscriptions.filter(nom__icontains=query_nom)  # Recherche insensible à la casse

    if query_date:
        inscriptions = inscriptions.filter(date_reservation=query_date)

    # Pagination
    paginator = Paginator(inscriptions, 5)  # 5 réservations par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'reservation/clients_list.html', {
        'page_obj': page_obj,
        'paginator':paginator,
        'page_number':page_number,
        'query_nom': query_nom,
        'query_date': query_date,
    })



def acceuil_dashboard(request):
    # Récupérer le nombre total de personnes inscrites
    total_inscriptions = Inscription.objects.count()

    # Récupérer le nombre total de réservations
    total_reservations = Reservation.objects.count()

    # Récupérer le nombre de personnes ayant donné une avance
    total_avances = Inscription.objects.filter(avance="oui").count()

    # Récupérer le nombre de clients inscrits aujourd'hui
    today = date.today()
    clients_today = Inscription.objects.filter(date=today).count()

    # Passer les statistiques au template
    context = {
        'total_inscriptions': total_inscriptions,
        'total_reservations': total_reservations,
        'total_avances': total_avances,
        'clients_today': clients_today,
    }

    return render(request, 'reservation/acceuil_dashboard.html', context)
