from django.test import TestCase

from core.models import GeographicBoundary
from .models import User, Organization


class UserTests(TestCase):

    def test_user_creation(self):
        user = User(email='name@example.com')
        user.save()
        self.assertIsInstance(user, User)


class OrganizationTests(TestCase):

    def test_organization_creation(self):
        area = GeographicBoundary(name='Pennsylvania')
        area.save()
        organization = Organization(name='March on Harrisburg', territory=area)
        organization.save()
        self.assertIsInstance(organization, Organization)
