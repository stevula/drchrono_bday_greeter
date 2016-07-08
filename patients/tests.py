import datetime

from django.test import TestCase

from .models import Patient, Doctor


# Create your tests here.
class PatientMethodTests(TestCase):
    def test_age(self):
        two_years_ago = datetime.datetime.now() - datetime.timedelta(days=730)
        patient = Patient(dob=two_years_ago)
        self.assertEqual(patient.age(), datetime.timedelta(2))
