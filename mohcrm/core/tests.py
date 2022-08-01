from django.test import TestCase


from .models import Site, Location, Organization, ContactInfo


class SiteTests(TestCase):

    def test_site_creation(self):
        site = Site()
        site.save()
        self.assertIsInstance(site, Site)


class LocationTests(TestCase):

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

