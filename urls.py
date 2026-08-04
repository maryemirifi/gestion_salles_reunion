from django.urls import path
from . import views

urlpatterns = [
    path('', views.salle_list, name='salle_list'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('reservation/ajouter/', views.reservation_create, name='reservation_create'),
    path('mes_reservations/', views.mes_reservations, name='mes_reservations'),
    path('reservation/modifier/<int:id>/', views.reservation_update, name='reservation_update'),
    path('reservation/supprimer/<int:id>/', views.reservation_delete, name='reservation_delete'),
    path('planning/', views.planning, name='planning'),
]