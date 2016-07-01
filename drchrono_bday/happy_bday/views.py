from django.shortcuts import render, HttpResponse
from.models import Patient


def welcome(request):
    return HttpResponse("Welcome!")


def index(request):
    patients = Patient.objects.all()
    output = ", ".join([p.name for p in patients])
    return HttpResponse(output)


def new(request):
    return HttpResponse("new")


def show(request, patient_id):
    return HttpResponse("show %s" % patient_id)
