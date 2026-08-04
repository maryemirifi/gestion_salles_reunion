from django.db import models
from django.contrib.auth.models import User

class Salle(models.Model):
    nom = models.CharField(max_length=100)
    capacite = models.PositiveIntegerField()
    localisation = models.CharField(max_length=150)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.nom  


    


class Reservation(models.Model):
    salle = models.ForeignKey(Salle, on_delete=models.CASCADE)
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()
    objet = models.CharField(max_length=100)
    nombre_personnes = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.objet} - {self.salle.nom}"