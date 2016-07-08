from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic


from.models import Patient, Doctor


class IndexView(generic.ListView):
    def get_queryset(self):
        """ All patients for currently signed in doctor """
        # TODO: get currently signed in doctor
        doctor = Doctor.objects.get(pk=1)
        return doctor.patient_set.all()


class DetailView(generic.DetailView):
    model = Patient


def add(request):
    # TODO: get currently signed in doctor
    doctor = Doctor.objects.get(pk=1)
    print request.POST
    form = request.POST
    doctor.patient_set.create(
        name=form['name'],
        dob=form['dob'],
        email=form['email'],
        phone=form['phone'])
    return HttpResponseRedirect(reverse('patients:index'))
