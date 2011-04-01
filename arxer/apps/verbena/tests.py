"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

import unittest
from verbena.models import Student

class StudentTestCase(unittest.TestCase):
    def setUp(self):
        self.bob = Student.objects.create(username='joe', password='that')
