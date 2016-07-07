from django.shortcuts import render, HttpResponse, get_object_or_404
from django.template import loader
from django.http import Http404

from.models import Patient, Doctor


def index(request):
    # TODO: get currently signed in doctor
    doctor = Doctor.objects.get(pk=1)

    # TODO: fetch patient data from api instead of form
    if request.method == 'POST':
        form = request.POST
        # create Patient
        doctor.patient_set.create(
            name=form['name'],
            dob=form['dob'],
            email=form['email'],
            phone=form['phone'])

    # TODO: get patients belonging to this doctor only
    patients = doctor.patient_set.all()
    return render(request, 'patients/index.html', {
        'patient_list': patients, 'doctor': doctor})


def show(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)
    return render(request, 'patients/show.html', {'patient': patient})
