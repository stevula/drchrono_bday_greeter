from django.shortcuts import render, HttpResponse
from django.template import loader

from.models import Patient


def welcome(request):
    return HttpResponse("Welcome!")


def index(request):
    patients = Patient.objects.all()
    return render(request, 'happy_bday/index.html', {'patient_list': patients})


def show(request, patient_id):
    try:
        patient = Patient.objects.get(pk=patient_id)
    except Patient.DoesNotExist:
        raise Http404("Patient does not exist")
    return render(request, 'happy_bday/show.html', {'patient': patient})


def new(request):
    return HttpResponse("new")
