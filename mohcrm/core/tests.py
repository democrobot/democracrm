from django.test import TestCase

from .utils import geocode_address
from .models import Site, Location, Organization, ContactInfo, Note


class UtilsTests(TestCase):

    def test_geocoder(self):
        input_address = '10 N 2nd St, Harrisburg, PA 17101'
        output_address = geocode_address(input_address)
        self.assertEquals(output_address['results'][0]['formatted_address'], input_address)


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
        site = Site()
        site.save()
        location = Location(site=site)
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
