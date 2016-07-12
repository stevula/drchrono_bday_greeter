import datetime
import pytz
import requests

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from happy_bday.settings import CLIENT_ID, REDIRECT_URI, CLIENT_SECRET

from .models import Patient, Doctor, User


# VIEWS

class IndexView(generic.ListView):
    def get_queryset(self):
        return Patient.objects.all()

    def get(self, request):
        user = current_user(request)
        return render(request, 'patients/patient_list.html', {
            'patient_list': self.get_queryset(), 'user': user})


class DetailView(generic.DetailView):
    model = Patient

    def get(self, request, **kwargs):
        user = current_user(request)
        patient = Patient.objects.get(pk=kwargs.get('pk'))
        return render(request, 'patients/patient_detail.html', {
            'patient': patient, 'user': user})


class SigninView(generic.View):
    template_name = 'patients/patient_signin.html'

    def get(self, request):
        url = 'https://drchrono.com/o/authorize/?redirect_uri=%s&response_type=code&client_id=%s' % (REDIRECT_URI, CLIENT_ID)
        return render(request, 'patients/patient_signin.html', {'url': url})


# VIEWLESS ACTIONS

def drchrono_signin(request):
    error = request.GET.get('error')
    if error:
        raise ValueError('Error authorizing application: %s' % error)

    code = request.GET.get('code')
    response = requests.post('https://drchrono.com/o/token/', data={
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    })
    response.raise_for_status()
    data = response.json()

    # Save these in your database associated with the user
    access_token = data['access_token']
    refresh_token = data['refresh_token']
    expires_timestamp = datetime.datetime.now(pytz.utc) + datetime.timedelta(seconds=data['expires_in'])

    response = requests.get('https://drchrono.com/api/users/current', headers={
        'Authorization': 'Bearer %s' % access_token,
    })
    response.raise_for_status()
    data = response.json()

    # You can store this in your database along with the tokens
    username = data['username']
    user = User.objects.get_or_create(username=username)[0]
    login(request, user)
    user.access_token = access_token
    user.refresh_token = refresh_token
    user.expires_timestamp = expires_timestamp
    user.save()

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


def login(request, user):
    request.session['user_pk'] = user.pk
    return None


def logout(request):
    request.session['user_pk'] = None
    return None


def current_user(request):
    return User.objects.get(pk=request.session['user_pk'])
