from django.shortcuts import render, HttpResponse, get_object_or_404
from django.template import loader
from django.http import Http404

from.models import Patient, Doctor


def index(request):
    # if request.method == 'POST':
    #     # create Patient
    #     Patient.create()
    # else:
        # handle GET
        # TODO: get currently signed in doctor
        doctor = Doctor.objects.get(pk=1)
        # TODO: get patients belonging to this doctor only
        patients = Patient.objects.all()
        return render(request, 'patient_mgr/index.html', {
            'patient_list': patients, 'doctor': doctor})


def show(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)
    # try:
    #     patient = Patient.objects.get(pk=patient_id)
    # except Patient.DoesNotExist:
    #     raise Http404("Patient does not exist.")
    return render(request, 'patient_mgr/show.html', {'patient': patient})


def new(request):
    return HttpResponse("new")


def create(request):
    return HttpResponse("Hi")
