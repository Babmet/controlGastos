from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse("¡Hola, mundo!")

def about(request):
    return HttpResponse("Acerca de nosotros")

def contact(request):
    return HttpResponse("Contáctanos")

