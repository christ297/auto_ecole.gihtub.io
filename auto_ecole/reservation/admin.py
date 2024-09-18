from django.contrib import admin
from .models import User,Reservation,Inscription
admin.site.register([User,Reservation,Inscription])