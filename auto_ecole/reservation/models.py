from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _


class User(models.Model):
    pass

class Reservation(models.Model):
    VEHICLE_CHOICES = [
        ('manual', 'Manuel'),
        ('automatic', 'Automatique'),
    ]
    
    nom = models.CharField(max_length=100)
    email = models.EmailField()
    #numero = PhoneNumberField(_("Numéro de téléphone"), blank=True, help_text="Entrez le numéro au format international, ex : +228 99 63 23 22")
    date_reservation = models.DateField()
    heure_reservation = models.TimeField()
    type_vehicule = models.CharField(max_length=10, choices=VEHICLE_CHOICES)

    def __str__(self):
        return f"Réservation de {self.nom} pour le {self.date_reservation} à {self.heure_reservation}"

class Transaction(models.Model):
    identifier = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=15)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    network = models.CharField(max_length=10, choices=[('FLOOZ', 'Flooz'), ('TMONEY', 'TMoney')])
    tx_reference = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction {self.identifier} - {self.phone_number}"

class Inscription(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    telephone = models.CharField(max_length=20)
    ville = models.CharField(max_length=100)
    categorie = models.CharField(max_length=50)
    formation = models.CharField(max_length=100)
    typecours = models.CharField(max_length=50)
    avance = models.CharField(max_length=10)  # Par exemple 'oui' ou 'non'
    
    def __str__(self):
        return f'{self.nom} {self.prenom}'