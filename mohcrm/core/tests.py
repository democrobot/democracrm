from django.test import TestCase

from .utils import geocode_address
from .models import Site, Location, Organization, ContactInfo, Note


class UtilsTests(TestCase):

    def test_geocoder(self):
        address = geocode_address('501 N 3rd St, Harrisburg, PA 17120')
        print(dir(address))
        address_components = {
            'number': '501', 'street': '3rd', 'suffix': 'St',
            'formatted_street': '3rd St', 'city': 'Harrisburg',
            'county': 'Dauphin County', 'state': 'PA', 'zip': '17113',
            'country': 'US'
        }
        self.assertEquals(address['results'][0], address_components)


class SiteTests(TestCase):

    def test_has_docstring(self):
        site = Site()
        self.assertIsNotNone(site.__doc__)

    def test_site_creation(self):
        site = Site()
        site.save()
        self.assertIsInstance(site, Site)


class LocationTests(TestCase):

    def test_has_docstring(self):
        site = Site()
        self.assertIsNotNone(site.__doc__)

    def test_location_creation(self):
        location = Location()
        location.save()
        self.assertIsInstance(location, Location)


class OrganizationTests(TestCase):

    def test_organization_creation(self):
        organization = Organization()
        organization.save()
        self.assertIsInstance(organization, Organization)


class ContactInfoTests(TestCase):

    def test_contactinfo_creation(self):
        contact_info = ContactInfo()
        contact_info.save()
        self.assertIsInstance(contact_info, ContactInfo)


class NoteTests(TestCase):

    def test_note_creation(self):
        note = Note()
        note.save()
        self.assertIsInstance(note, Note)
