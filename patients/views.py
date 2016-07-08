from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.core.urlresolvers import reverse
from django.views import generic

from.models import Patient, Doctor


class IndexView(generic.ListView):
    template_name = 'patients/index.html'
    context_object_name = 'patient_list'

    def get_queryset(self):
        """ All patients for currently signed in doctor """
        # TODO: get currently signed in doctor
        doctor = Doctor.objects.get(pk=1)
        return doctor.patient_set.all()

    # TODO: fetch patient data from api instead of form
    # if request.method == 'POST':
    #     form = request.POST
    #     # create Patient
    #     doctor.patient_set.create(
    #         name=form['name'],
    #         dob=form['dob'],
    #         email=form['email'],
    #         phone=form['phone'])
    #     return HttpResponseRedirect(reverse('patients:index'))


class DetailView(generic.DetailView):
    model = Patient
    template_name = 'patients/detail.html'
    # patient = get_object_or_404(Patient, pk=patient_id)
    # return render(request, 'patients/show.html', {'patient': patient})
