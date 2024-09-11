from django.shortcuts import render,HttpResponse

def home(request):
    return render(request,"learning/home.html")

def all_quizz(request):
    return render(request,"learning/all_quizz.html")

def register(request):
    return render(request,"learning/register.html")

def profile(request):
    return render(request,"learning/profile.html")