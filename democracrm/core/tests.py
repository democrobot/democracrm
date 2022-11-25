from django.test import TestCase

from .models import (
    Boundary,
    Site,
    Location,
    ContactInfo,
    Comment,
    Link,
)
from .utils import geocode_address


class BoundaryTests(TestCase):

    def test_boundary_creation(self):
        boundary = Boundary(name='Pennsylvania')
        boundary.save()
        self.assertIsInstance(boundary, Boundary)


class SiteTests(TestCase):

    def test_has_docstring(self):
        site = Site(name='Example Site')
        self.assertIsNotNone(site.__doc__)

    def test_site_creation(self):
        site = Site()
        site.save()
        self.assertIsInstance(site, Site)

    def test_site_physical_address(self):
        site = Site(
            name='PA State Capitol Complex',
            physical_street_number='501',
            physical_street_direction='N',
            physical_street_name='3rd',
            physical_street_suffix='St',
            physical_city='Harrisburg',
            physical_state='PA',
            physical_zip_code='17120'
        )
        site.save()
        address = '501 N 3rd St Harrisburg PA 17120'
        self.assertEquals(site.full_physical_address(), address)

    def test_site_mailing_address(self):
        site = Site(
            name='PA Treasury - Unclaimed Property',
            mailing_po_box='P.O. Box 1837',
            mailing_city='Harrisburg',
            mailing_state='PA',
            mailing_zip_code='17105-1837'
        )
        site.save()
        address = 'P.O. Box 1837 Harrisburg PA 17105-1837'
        self.assertEquals(site.full_mailing_address(), address)

    def test_site_coordinates(self):
        # Coordinates for PA Capitol based on Wikipedia
        # https://en.wikipedia.org/wiki/Pennsylvania_State_Capitol
        site = Site(
            name='PA State Capitol Complex',
            physical_latitude=40.264444,
            physical_longitude=-76.883611
        )
        site.save()
        coordinates = (40.264444, -76.883611)
        self.assertEquals(site.physical_coordinates(), coordinates)


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


class ContactInfoTests(TestCase):

    def test_contact_info_creation(self):
        contact_info = ContactInfo()
        contact_info.save()
        self.assertIsInstance(contact_info, ContactInfo)


class CommentTests(TestCase):

    def test_note_creation(self):
        comment = Comment(text='This is a test.')
        comment.save()
        self.assertIsInstance(comment, Comment)


class LinkTests(TestCase):

    def test_link_creation(self):
        link = Link(name='March on Harrisburg Website', url='https://www.mohpa.org')
        link.save()
        self.assertIsInstance(link, Link)

# Utility module tests


class UtilsTests(TestCase):

    def test_geocoder(self):
        input_address = '10 N 2nd St, Harrisburg, PA 17101'
        output_address = geocode_address(input_address)
        self.assertEquals(output_address['results'][0]['formatted_address'], input_address)
