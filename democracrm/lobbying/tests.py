from django.test import TestCase

from core.models import GeographicBoundary
from organizing.models import Organization
from organizing.tests import init_campaign

from .models import (
    GoverningBody,
    PoliticalSubdivision,
    PublicOfficial,
    SupportLevel,
)


class GoverningBodyTests(TestCase):

    def test_create_governing_body(self):
        boundary = GeographicBoundary(name='Pennsylvania')
        boundary.save()
        governing_body = GoverningBody(name='Example Body', boundary=boundary)
        governing_body.save()

        self.assertIsInstance(governing_body, GoverningBody)


class PoliticalSubdivisionTests(TestCase):

    def test_political_subdivision_creation(self):
        boundary = GeographicBoundary(name='Pennsylvania')
        boundary.save()
        governing_body = GoverningBody(name='Pennsylvania State Government', boundary=boundary)
        governing_body.save()

        political_subdivision = PoliticalSubdivision()
        political_subdivision.save()

        self.assertEquals(political_subdivision.seats, 1)

    def test_seat_assignments(self):
        """
        Ensure the number of officials is not larger than a subdivision's number of seats.
        :return:
        """
        political_subdivision = PoliticalSubdivision(name='Example District', seats=1)
        political_subdivision.save()

        official1 = PublicOfficial(first_name='Jane', last_name='Doe',
                                  subdivision=political_subdivision)
        official1.save()
        official2 = PublicOfficial(first_name='John', last_name='Smith',
                                   subdivision=political_subdivision)
        official2.save()


class PublicOfficialTests(TestCase):

    def test_public_official_creation(self):
        official = PublicOfficial(first_name='Jane', last_name='Doe')
        official.save()
        self.assertEquals(official.role, 'Legislator')

    def test_subdivision_assignment(self):
        political_subdivision = PoliticalSubdivision(name='Example District')
        political_subdivision.save()
        official = PublicOfficial(first_name='Jane', last_name='Doe', subdivision=political_subdivision)
        official.save()

        self.assertEquals(official.subdivision, political_subdivision)


class SupportLevelTests(TestCase):

    def test_support_level_creation(self):
        campaign = init_campaign()
        official = init_public_official()
        support_level = SupportLevel(campaign=campaign, official=official)
        support_level.save()
        self.assertIsInstance(support_level, SupportLevel)


def init_public_official():
    official = PublicOfficial(first_name='Jane', last_name='Doe')
    official.save()

    return official
