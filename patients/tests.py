import datetime

from django.test import TestCase
from django.core.urlresolvers import reverse

from .models import Patient, Doctor


def create_doctor():
    return Doctor.objects.create(name="Test Doctor")


def create_patients(doctor):
    patient_1 = doctor.patient_set.create(name="Test Patient 1")
    patient_2 = doctor.patient_set.create(name="Test Patient 2")
    patient_3 = doctor.patient_set.create(name="Test Patient 3")
    return patient_1, patient_2, patient_3


def create_both():
    doctor = create_doctor()
    patients = create_patients(doctor)
    return doctor, patients


class PatientMethodTests(TestCase):
    def test_age(self):
        two_years_ago = datetime.datetime.now() - datetime.timedelta(days=730)
        patient = Patient(dob=two_years_ago)
        self.assertEqual(patient.age(), datetime.timedelta(2))


class PatientIndexViewTests(TestCase):
    def test_index_view_with_no_patients(self):
        """Displays a message if no patients exist."""
        create_doctor()
        response = self.client.get(reverse('patients:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No patients found.")
        self.assertQuerysetEqual(response.context['patient_list'], [])

    # def test_doctor_sees_own_patients_only(self):
    #     """Doctor/user sees only own patients listed."""
    #     doctor_1 = create_doctor()
    #     patients_1 = create_patients(doctor_1)
    #     doctor_2 = create_doctor()
    #     patients_2 = create_patients(doctor_2)
    #     # TODO: need user system so can view as doctor_1
    #     response = self.client.get(reverse('patients:index'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertQuerysetEqual(response.context['patient_list'], [])


class PatientDetailViewTests(TestCase):
    def test_detail_view_with_nonexisting_patient(self):
        """
        Renders 404 page when visiting detail page for patient who doesn't exist.
        """
        url = reverse('patients:detail', args=(1,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_detail_view_with_existing_patient(self):
        """Renders patient info when patient does exist."""
        create_both()
        url = reverse('patients:detail', args=(1,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


# check that new patients are updated correctly
