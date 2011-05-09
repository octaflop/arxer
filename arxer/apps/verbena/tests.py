"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.

TODO:
    - add invalid test cases with assertnotcontains
    - add a permission inspector function to each test-case
    - add a general login inspector for an anonymous client
"""

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from verbena.models import Student, Faculty, Organization, Location, Member

class StudentTestCase(TestCase):
    fixtures = ['dev.json']
    def setUp(self):
        self.u = User.objects.create(username='bob', password='that', first_name='Bob',
        last_name='Exampler')
        self.bob = Student.objects.create(user=self.u)
        self.c = Client()

    def test_url(self):
        url = "/members/students/%s" % self.bob.slug
        response = self.c.get(url)
        self.assertContains(response, self.u.username)

class FacultyTestCase(TestCase):
    def setUp(self):
        self.u = User.objects.create(username='julie', password='that',
        first_name='Julie', last_name='example')
        self.julie = Faculty.objects.create(user=self.u)
        self.c = Client()

    def test_url(self):
        url = "/members/faculty/%s" % self.julie.slug
        response = self.c.get(url)
        self.assertContains(response, self.u.username)

class OrganizationTestCase(TestCase):
    def setUp(self):
        self.u = User.objects.create(username='hippieclub', password='that',
            first_name='', last_name='')
        self.bob = User.objects.create(username='BobMarley',
            password='that', first_name='Bob', last_name='Marley')
        self.leader = Member.objects.create(user=self.bob)
        self.location =  Location.objects.create(place='Vancouver')
        self.hippies = Organization.objects.create(user=self.u,
            leader=self.leader, location=self.location, title="The Hippies")
        self.c = Client()
    def test_page_disp(self):
        url = "/organization/%s" % self.hippies.slug
        response = self.c.get(url)
        self.assertContains(response, self.hippies.title)
