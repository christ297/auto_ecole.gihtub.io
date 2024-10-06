
from . import views
from django.urls import path
from django.views.generic import TemplateView  # Assure-toi d'avoir cet import



urlpatterns = [
    path("reservation",views.reservation_view,name="reservation"),
    path('success/', TemplateView.as_view(template_name="reservation/reservation_success.html"), name='reservation_success'),
    path('admin-login/', views.admin_login_view, name='admin_login'),
    path('clients/', views.clients_list_view, name='clients'),
    path('paiement/', views.initiate_payment, name='payment'),
    path('paiement/success/<int:transaction_id>/', views.payment_success, name='payment_success'),
    path('',views.aceuill,name="index"),
    path('inscription',views.inscription,name="inscription"),
    path('clients_inscrits',views.inscription_list_view,name="inscription_list"),
    path('dashboard',views.dashboard,name="dashboard"),
    path('aceuill_dashboard',views.acceuil_dashboard,name="acceuil_dashboard"),
    path('avance',views.avance_list_view,name="avance"),
    path('logout',views.logout_view,name="logout"),

]
