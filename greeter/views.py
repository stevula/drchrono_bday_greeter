import datetime
import pytz
import requests
import drchrono

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from django.views import generic
from drchrono_bday_greeter.settings import (
    CLIENT_ID, REDIRECT_URI, CLIENT_SECRET)

from .models import User, Greeting
from helpers import *


# VIEWS

class IndexView(generic.ListView):
    def get_greetings_for_today(self):
        today = datetime.datetime.today()
        day = today.day
        month = today.month
        matches = Greeting.objects.filter(
            birth_day=day,
            birth_month=month
        )
        return matches

    def get(self, request):
        new_patients = []
        birthday_patients = []
        user = request.user
        # user is authenticated on successful redirect from drchrono
        if user.is_authenticated():
            patients = drchrono.get_patients(user.access_token)
            new_patients = enroll_new_patients(patients)
            greetings_today = self.get_greetings_for_today()
            # TODO: refactor duplication
            return render(request, 'greeter/greeter_list.html', {
                'greetings_today': greetings_today,
                'new_patients': new_patients,
                'user': user
                })
        return render(request, 'greeter/greeter_list.html', {'user': user})


class SigninView(generic.View):
    template_name = 'greeter/greeter_signin.html'

    def get(self, request):
        url = 'https://drchrono.com/o/authorize/?redirect_uri=%s&response_type=code&client_id=%s' % (
            REDIRECT_URI, CLIENT_ID)

        return render(request, 'greeter/greeter_signin.html', {
            'user': None, 'url': url})


# SESSIONS
# TODO: use built-in auth
# def signin(request, user):
#     request.session['user_pk'] = user.pk
#     return user


# def signout(request):
#     request.session['user_pk'] = None
#     return HttpResponseRedirect(reverse('greeter:index'))


# def current_user(request):
#     try:
#         pk = request.session['user_pk']
#         return User.objects.get(pk=pk)
#     except:
#         return None


# DRCHRONO OAUTH (no view)

def drchrono_redirect(request):
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
    user = authenticate(username=user.username)
    if user is not None:
        if user.is_active:
            login(request, user)
        # TODO: handle inactive users
    # TODO: else error message
    return HttpResponseRedirect(reverse('greeter:index'))
