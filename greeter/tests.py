import datetime

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.sessions.models import Session

from .models import Greeting, User
from .views import drchrono_redirect, create_user_or_update_tokens


def create_user():
    return User.objects.create()


def create_greeting(birthday):
    return Greeting.objects.create()


def signin_user(session, user):
    session['user_pk'] = user.pk
    session.save()


class IndexViewTests(TestCase):
    def test_logged_out_user_sees_no_patients(self):
        """Logged out user cannot see patients"""
        response = self.client.get(reverse('greeter:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['birthday_patients'], [])
        self.assertQuerysetEqual(response.context['new_patients'], [])

    def test_index_view_without_bdays_today(self):
        """Displays an appropriate message if there are no birthdays today"""
        user = create_user()
        session = self.client.session
        signin_user(session, user)
        response = self.client.get(reverse('greeter:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No patients with birthdays today.")
        self.assertQuerysetEqual(response.context['birthday_patients'], [])

    def test_index_view_with_bdays_today(self):
        """Displays an appropriate message if no birthdays today."""
        today = datetime.datetime.today()
        create_greeting(birthday=today)
        signin_user()
        response = self.client.get(reverse('greeter:index'))
        print response
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No patients with birthdays today.")
        self.assertQuerysetEqual(response.context['birthday_patients'], [])


class SigninViewTests(TestCase):
    def test_signin_view_exists(self):
        """Renders signin form."""
        url = reverse('greeter:signin')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


# TODO
# check that new patients are updated correctly - new_patients list
# leapyear bday
# auth tests
# oauth tests?
# current_user
# signin/signout
# drchrono functions
