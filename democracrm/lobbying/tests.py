from django.test import TestCase

from places.models import Boundary
from organizing.models import Organization
from organizing.tests import init_campaign

from .models import (
    GoverningBody,
    PoliticalSubdivision,
    PublicOfficial,
    SupportLevel,
    InterpersonalTie,
)


class GoverningBodyTests(TestCase):

    def test_create_governing_body(self):
        boundary = Boundary(name='Pennsylvania')
        boundary.save()
        governing_body = GoverningBody(name='Example Body', boundary=boundary)
        governing_body.save()

        self.assertIsInstance(governing_body, GoverningBody)


class PoliticalSubdivisionTests(TestCase):

    def test_political_subdivision_creation(self):
        boundary = Boundary(name='Pennsylvania')
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
        self.fail()


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


def init_public_official(first_name='Jane', last_name='Doe'):
    official = PublicOfficial(first_name=first_name, last_name=last_name)
    official.save()

    return official


class InterpersonalTieTests(TestCase):

    def test_interpersonal_tie_creation(self):
        official1 = init_public_official(first_name='Official', last_name='One')
        official2 = init_public_official(first_name='Official', last_name='Two')
        tie = InterpersonalTie(official1=official1, official2=official2)
        tie.save()
        self.assertIsInstance(tie, InterpersonalTie)

    def test_interpersonal_tie_relationship_summary(self):
        official1 = init_public_official(first_name='Official', last_name='One')
        official2 = init_public_official(first_name='Official', last_name='Two')
        tie = InterpersonalTie(official1=official1, official2=official2)
        tie.save()
        self.assertEquals(tie.relationship_summary(), 'Official One is unknown/neutral towards Official Two')

    def test_interpersonal_ties_to(self):
        official1 = init_public_official(first_name='Official', last_name='One')
        official2 = init_public_official(first_name='Official', last_name='Two')
        official3 = init_public_official(first_name='Official', last_name='Three')
        tie1 = InterpersonalTie(official1=official1, official2=official2)
        tie1.save()
        tie2 = InterpersonalTie(official1=official1, official2=official3)
        tie2.save()
        ties = official1.ties_from.all()
        self.assertIn(tie1, ties)
        self.assertIn(tie2, ties)

    def test_interpersonal_ties_from(self):
        official1 = init_public_official(first_name='Official', last_name='One')
        official2 = init_public_official(first_name='Official', last_name='Two')
        official3 = init_public_official(first_name='Official', last_name='Three')
        tie1 = InterpersonalTie(official1=official1, official2=official3)
        tie1.save()
        tie2 = InterpersonalTie(official1=official2, official2=official3)
        tie2.save()
        ties = official3.ties_to.all()
        self.assertIn(tie1, ties)
        self.assertIn(tie2, ties)
