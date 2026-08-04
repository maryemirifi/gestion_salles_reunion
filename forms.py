from django import forms
from .models import Reservation 


from django.core.exceptions import ValidationError
from django.utils import timezone

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = [
            "salle",
            "date",
            "heure_debut",
            "heure_fin",
            "objet",
            "nombre_personnes"
        ]
        

        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "heure_debut": forms.TimeInput(attrs={"type": "time"}),
            "heure_fin": forms.TimeInput(attrs={"type": "time"}),
            "objet": forms.TextInput(attrs={"placeholder": "Objet de la réservation"}),
        }

    def clean_date(self):
        date = self.cleaned_data.get("date")

        if date and date < timezone.localdate():
            raise ValidationError(
                "La date de réservation ne peut pas être dans le passé."
            )

        return date

    def clean(self):
        cleaned_data = super().clean()

        salle = cleaned_data.get("salle")
        date = cleaned_data.get("date")
        heure_debut = cleaned_data.get("heure_debut")
        heure_fin = cleaned_data.get("heure_fin")

        if heure_debut and heure_fin:
            if heure_fin <= heure_debut:
                raise ValidationError(
                    "L'heure de fin doit être postérieure à l'heure de début."
                )

        # Vérification des conflits de réservation
        if salle and date and heure_debut and heure_fin:
            conflit = Reservation.objects.filter(
                salle=salle,
                date=date,
                heure_debut__lt=heure_fin,
                heure_fin__gt=heure_debut,
            )

            # Exclure l'objet courant en cas de modification
            if self.instance.pk:
                conflit = conflit.exclude(pk=self.instance.pk)

            if conflit.exists():
                raise ValidationError(
                    "Cette salle est déjà réservée sur ce créneau."
                )

        return cleaned_data


def clean(self):
    cleaned_data = super().clean()

    heure_debut = cleaned_data.get('heure_debut')
    heure_fin = cleaned_data.get('heure_fin')

    if heure_debut and heure_fin:
        if heure_fin <= heure_debut :
            raise forms.ValidationError("l'heure de fin doit être supérieure à l'heure de début.")
    
    salle = cleaned_data.get('salle')
    date = cleaned_data.get('date')

    if salle and date and heure_debut and heure_fin :
        conflits : Reservation.objects.filter(
             salle=salle,
             date=date,
             heure_debut__It=heure_fin,
             heure_fin__gt=heure_debut,
             )
        if self.instance.pk:
             conflits = conflits.exclude(pk=self.instance.pk)
                                            
        if conflits.exists():
            raise forms.ValidationError("Cette salle est déja réservée pendant cette période ")
        

        return cleaned_data

