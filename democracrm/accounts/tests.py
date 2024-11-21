from django.test import TestCase

from .models import UserAccount, OrganizationAccount
from people.models import Contact
from places.models import Boundary


class UserAccountTests(TestCase):

    def test_user_account_creation(self):
        user = UserAccount(email='name@example.com', password='abc123')
        user.save()
        self.assertIsInstance(user, UserAccount)


class OrganizationAccountTests(TestCase):

    def test_organization_account_creation(self):
        boundary = Boundary(name='Pennsylvania')
        boundary.save()
        contact = Contact()
        contact.save()
        org_account = OrganizationAccount(
            name='March on Harrisburg',
            territory=boundary,
            #primary_contact=contact
        )
        org_account.save()
        self.assertIsInstance(org_account, OrganizationAccount)


def init_user_account():
    user_account = UserAccount(email='name@example.com', password='abc123')
    user_account.save()
    return user_account
