from django.test import TestCase

from .models import UserAccount, OrganizationAccount
from contacts.models import ContactInfo
from places.models import Boundary


class UserTests(TestCase):

    def test_user_creation(self):
        user = UserAccount(email='name@example.com', password='abc123')
        user.save()
        self.assertIsInstance(user, UserAccount)


class OrganizationTests(TestCase):

    def test_organization_creation(self):
        boundary = Boundary(name='Pennsylvania')
        boundary.save()
        contact = ContactInfo()
        contact.save()
        org_account = OrganizationAccount(
            name='March on Harrisburg',
            territory=boundary,
            primary_contact=contact
        )
        org_account.save()
        self.assertIsInstance(org_account, OrganizationAccount)
