from django.test import TestCase

from .models import ContactRole, ContactInfo


class ContactInfoTests(TestCase):

    def test_contact_info_creation(self):
        contact_info = ContactInfo()
        contact_info.save()
        self.assertIsInstance(contact_info, ContactInfo)
