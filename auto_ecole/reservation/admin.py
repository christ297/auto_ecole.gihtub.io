from django.contrib import admin
from .models import User,Reservation
admin.site.register([User,Reservation])