import datetime
import pytz
import requests

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.views import generic
from happy_bday.settings import CLIENT_ID, REDIRECT_URI, CLIENT_SECRET

from .models import User, Greeting


# VIEWS

class IndexView(generic.ListView):
    def get_queryset(self, request):
        patients = []
        if current_user(request):
            patients = get_patients(current_user(request).access_token)
        return patients

    def get(self, request):
        user = current_user(request)
        patients = []

        return render(request, 'patients/patient_list.html', {
            'patient_list': self.get_queryset(request), 'user': user})


class SigninView(generic.View):
    template_name = 'patients/patient_signin.html'

    def get(self, request):
        url = 'https://drchrono.com/o/authorize/?redirect_uri=%s&response_type=code&client_id=%s' % (REDIRECT_URI, CLIENT_ID)
        return render(request, 'patients/patient_signin.html', {'user': None, 'url': url})


# USERS

def create_user_or_update_tokens(data):
    access_token = data['access_token']
    refresh_token = data['refresh_token']
    expires_timestamp = datetime.datetime.now(pytz.utc) + datetime.timedelta(seconds=data['expires_in'])

    user_info = get_user_info(access_token)
    username = user_info['username']
    user = User.objects.get_or_create(username=username)[0]
    user.access_token = access_token
    user.refresh_token = refresh_token
    user.expires_timestamp = expires_timestamp
    user.save()
    return user


# GREETINGS

def register_for_greetings(patients):
    new_patients = []
    for patient in patients:
        try:
            Greeting.objects.get(patient_id=patient['id'])
        except ObjectDoesNotExist:
            new_greeting = Greeting.objects.create(
                doctor_id=patient['doctor'],
                patient_id=patient['id'],
                first_name=patient['first_name'],
                last_name=patient['last_name'],
                dob=patient['date_of_birth'],
                email=patient['email']
            )
            new_patients.append(new_greeting)
    print new_patients
    return new_patients


# SESSIONS

def signin(request, user):
    request.session['user_pk'] = user.pk
    return user


def signout(request):
    request.session['user_pk'] = None
    return HttpResponseRedirect(reverse('patients:index'))


def current_user(request):
    try:
        pk = request.session['user_pk']
        return User.objects.get(pk=pk)
    except:
        return None


# DRCHRONO


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
    user = create_user_or_update_tokens(data)
    signin(request, user)
    return HttpResponseRedirect(reverse('patients:index'))


def get_user_info(access_token):
    response = requests.get('https://drchrono.com/api/users/current', headers={
        'Authorization': 'Bearer %s' % access_token,
    })
    response.raise_for_status()
    return response.json()


def get_patients(access_token):
    headers = {
        'Authorization': 'Bearer %s' % access_token,
    }

    patients = []
    patients_url = 'https://drchrono.com/api/patients?verbose=true'
    while patients_url:
        data = requests.get(patients_url, headers=headers).json()
        patients.extend(data['results'])
        patients_url = data['next']  # A JSON null on the last page
    register_for_greetings(patients)
    return patients
