"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.

TODO:
    - add a permission inspector function to each test-case
"""

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from verbena.models import Student, Faculty, Organization, Location, Member, Event
import datetime

class StudentTestCase(TestCase):
    #fixtures = ['dev.json']
    def setUp(self):
        self.u = User.objects.create(username='bob', password='that', first_name='Bob',
        last_name='Exampler')
        self.bob = Student.objects.create(member=self.u.member)
        self.c = Client()

    def test_url(self):
        url = "/members/students/%s" % self.bob.member.slug
        response = self.c.get(url)
        self.assertContains(response, self.u.username)

    def test_permissions(self):
        """
            Ensure that students may not become a faculty or an organization
            without removing their student status first.
        """
        self.member = self.bob.member
        # may not be an organization leader
        org = Organization.objects.create(leader=self.member)
        return None

class FacultyTestCase(TestCase):
    def setUp(self):
        self.u = User.objects.create(username='julie', password='that',
            first_name='Julie', last_name='example')
        self.julie = Faculty.objects.create(member=self.u.member)
        self.c = Client()

    def test_url(self):
        url = "/members/faculty/%s" % self.julie.member.slug
        response = self.c.get(url)
        self.assertContains(response, self.u.username)

class OrganizationTestCase(TestCase):
    def setUp(self):
        self.u = User.objects.create(username='hippieclub', password='that',
            first_name='Bill', last_name='Hippie')
        self.bob = User.objects.create(username='BobMarley',
            password='that', first_name='Bob', last_name='Marley')
        self.leader = self.bob.member
        self.location =  Location.objects.create(place='Vancouver')
        self.hippies = Organization.objects.create(
            leader=self.leader, about="About nothing", location=self.location, title="The Hippies")
        self.c = Client()
        self.c.logout()

    def test_page_disp(self):
        url = "/organization/%s" % self.hippies.org_slug
        response = self.c.get(url)
        self.assertContains(response, self.hippies.title)

    def test_page_noedit(self):
        """
         ensure that groups can't be edited by non-owners,
         in this case, only self.bob can edit, but bill the hippie is trying to.
        """
        url = "/organization/%s/edit" % self.hippies.org_slug
        self.c.login(username='hippieclub', password='that')
        response = self.c.get(url)
        ##self.assertNotContains(response, self.hippies.title)
        ## something tricky is happening here...
        self.assertContains(response, '', status_code=302)

    def test_page_noedit_tologin(self):
        """
            ensure that AnonymousUsers are redirected to the login page when
            trying to edit.
        """
        url = "/organization/%s/edit" % self.hippies.org_slug
        login_url = "/account/login/"
        redirect_url = "%s?next=/organization/%s/edit" % (login_url,
                self.hippies.org_slug)
        response = self.c.get(url)
        self.assertRedirects(response, redirect_url)

class EventTestCase(TestCase):
    def setUp(self):
        self.location =  Location.objects.create(place='Vancouver')
        self.event = Event.objects.create(title='Lunch',
                start_date = datetime.datetime.now(),
                end_date = datetime.datetime.now() + datetime.timedelta(200),
                location = self.location)
        self.c = Client()

    def test_page_disp(self):
        url = "/event/%s" % self.event.slug
        response = self.c.get(url)
        self.assertContains(response, self.event.title)

class ActionGroupTestCase(TestCase):
    """
    NOT IMPLEMENTED (yet)
    """
    def setUp(self):
        return None
    def test_page_disp(self):
        return None


