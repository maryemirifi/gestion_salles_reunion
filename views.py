from django.shortcuts import render
from .models import Salle 
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required 
from .forms import ReservationForm 
from .models import Reservation
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib import messages
from itertools import groupby

@login_required
def salle_list(request):
    salles = Salle.objects.all()

    context = {
        'salles': salles,
    }

    return render(request, 'reservations/salle_list.html', context)


@login_required
def reservation_create(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)

        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.utilisateur = request.user

            if reservation.nombre_personnes > reservation.salle.capacite:
                messages.error(
                  request,
                 "Le nombre de personnes dépasse la capacité de la salle."
        )
            else:
                 reservation.save()
                 messages.success(request, "La réservation a été ajoutée avec succès.")
                 return redirect('mes_reservations')
    
        else:
            print(form.errors)

    else:
        form = ReservationForm()

    context = {
        'form': form,
    }

    return render(request, 'reservations/reservation_form.html', context)


@login_required
def mes_reservations(request):
    reservations = Reservation.objects.filter(utilisateur=request.user)

    context = {
        'reservations': reservations,
    }
    return render(request , 'reservations/mes_reservations.html', context)


@login_required
def reservation_update(request, id):
    reservation = get_object_or_404(
        Reservation, 
        id=id,
         utilisateur=request.user)

    if request.method =='POST':
       form = ReservationForm(request.POST, instance=reservation)

       if form.is_valid():
           form.save()
           messages.success(request, "La réservation a été modifiée avec succès.")
           return redirect('mes_reservations')
    
    else :
         form = ReservationForm(instance=reservation)
    

    context = {
    'form': form,
        }
    return render(request, 'reservations/reservation_form.html', context)


@login_required
def reservation_delete(request, id):
    reservation = get_object_or_404(
        Reservation,
        id=id,
        utilisateur=request.user)

    if request.method == "POST":
        reservation.delete()
        messages.success(request, "La réservation a été supprimée avec succès.")
        return redirect('mes_reservations')

    context = {
        'reservation': reservation,
    }

    return render(request,'reservations/reser_confirm_delete.html', context)


@login_required
def planning(request):
    reservations = Reservation.objects.all().order_by('date', 'heure_debut')

    reservations_par_jour = {}

    for date, groupe in groupby(reservations, key=lambda r: r.date):
        reservations_par_jour[date] = list(groupe)

    context = {
        'reservations_par_jour': reservations_par_jour
    }

    return render(request, 'reservations/planning.html', context)

    
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('salle_list')

    else:
        form = AuthenticationForm()

    context = {
        'form': form,
    }

    return render(request, 'reservations/login.html', context)



def logout_view(request):
    logout(request)
    return redirect('login')


 

