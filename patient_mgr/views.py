from django.shortcuts import render, HttpResponse, get_object_or_404
from django.template import loader
from django.http import Http404

from.models import Patient, Doctor


def index(request):
    # TODO: get currently signed in doctor
    doctor = Doctor.objects.get(pk=1)

    if request.method == 'POST':
        form = request.POST
        # create Patient
        doctor.patient_set.create(
            name=form['name'],
            dob=form['dob'],
            email=form['email'],
            phone=form['phone'])

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
