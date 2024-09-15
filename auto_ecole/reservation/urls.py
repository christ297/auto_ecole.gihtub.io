
from . import views
from django.urls import path
from django.views.generic import TemplateView  # Assure-toi d'avoir cet import



urlpatterns = [
    path("",views.reservation_view,name="reservation"),
    path('success/', TemplateView.as_view(template_name="reservation/reservation_success.html"), name='reservation_success'),
    path('admin-login/', views.admin_login_view, name='admin_login'),
    path('clients/', views.clients_list_view, name='clients'),
    path('paiement/', views.payment_view, name='payment'),
    path('paiement/success/<int:transaction_id>/', views.payment_success, name='payment_success'),
    path('paiement/echec/', views.payment_failed, name='payment_failed'),
    path('aceuill',views.aceuill,name="index"),

]
