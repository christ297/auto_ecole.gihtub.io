from django.db import models

class User(models.Model):
    pass

class Reservation(models.Model):
    VEHICLE_CHOICES = [
        ('manual', 'Manuel'),
        ('automatic', 'Automatique'),
    ]
    
    nom = models.CharField(max_length=100)
    email = models.EmailField()
    date_reservation = models.DateField()
    heure_reservation = models.TimeField()
    type_vehicule = models.CharField(max_length=10, choices=VEHICLE_CHOICES)

    def __str__(self):
        return f"Réservation de {self.nom} pour le {self.date_reservation} à {self.heure_reservation}"
