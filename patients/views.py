from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
import drchrono

from .models import Patient, Doctor


# VIEWS

class IndexView(generic.ListView):
    def get_queryset(self):
        """ All patients for currently signed in doctor """
        # TODO: get currently signed in doctor
        doctor = Doctor.objects.get(pk=1)
        return doctor.patient_set.all()


class DetailView(generic.DetailView):
    model = Patient


class SigninView(generic.View):
    template_name = 'patients/patient_signin.html'

    def get(self, request):
        return render(request, 'patients/patient_signin.html', {
            'redirect_uri': drchrono.REDIRECT_URI,
            'client_id': drchrono.CLIENT_ID
            })


# VIEWLESS ACTIONS

def drchrono(request, code):
    print code
    return HttpResponseRedirect(reverse('patients:index'))


def create(request):
    # TODO: get currently signed in doctor
    doctor = Doctor.objects.get(pk=1)
    form = request.POST
    doctor.patient_set.create(
        name=form['name'],
        dob=form['dob'],
        email=form['email'],
        phone=form['phone'])
    # TODO: redirect to patient show?
    return HttpResponseRedirect(reverse('patients:index'))


def destroy(request):
    # TODO: get specific patient
    patient = Patient.objects.get(pk=1)
    return HttpResponseRedirect(reverse('patients:index'))
