import datetime
import pytz
import drchrono

from django.core.exceptions import ObjectDoesNotExist
from .models import User, Greeting


def enroll_new_patients(patients):
    new_patients = []
    for patient in patients:
        try:
            Greeting.objects.get(patient_id=patient['id'])
        except ObjectDoesNotExist:
            # TODO: refactor this part into a function
            dob = patient['date_of_birth']
            day = None
            month = None
            if dob:
                dob = datetime.datetime.strptime(dob, '%Y-%m-%d')
                day = dob.day
                month = dob.month

            Greeting.objects.create(
                doctor_id=patient['doctor'],
                patient_id=patient['id'],
                first_name=patient['first_name'],
                last_name=patient['last_name'],
                email=patient['email'],
                birth_day=day,
                birth_month=month
            )
            new_patients.append(patient)
    return new_patients


def create_user_or_update_tokens(data):
    access_token = data['access_token']
    refresh_token = data['refresh_token']
    expires_timestamp = datetime.datetime.now(pytz.utc) + datetime.timedelta(
        seconds=data['expires_in'])

    user_info = drchrono.get_user_info(access_token)
    username = user_info['username']
    user = User.objects.get_or_create(username=username)[0]
    user.access_token = access_token
    user.refresh_token = refresh_token
    user.expires_timestamp = expires_timestamp
    user.save()
    return user