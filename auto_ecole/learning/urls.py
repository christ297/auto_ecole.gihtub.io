from django.urls import path
from . import views

urlpatterns = [
    path('home',views.home,name="home" ),
    path('all_quizz',views.all_quizz,name="all_quizz"),
    path('register',views.register,name="register"),
    path('profile',views.profile,name="profile"),
]