from django.test import TestCase

from .models import Contact, ContactRole, ContactGroup


class ContactTests(TestCase):

    def test_contact_info_creation(self):
        contact_info = Contact()
        contact_info.save()
        self.assertIsInstance(contact_info, Contact)
