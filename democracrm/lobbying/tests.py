from django.test import TestCase

from places.models import Boundary
from organizing.models import Organization
from organizing.tests import init_campaign

from .models import (
    Committee,
    GoverningBody,
    InterpersonalTie,
    Legislation,
    LegislativeSession,
    PoliticalParty,
    PoliticalSubdivision,
    PublicOffice,
    PublicOfficial,
    SupportLevel,
    Voter
)


class GoverningBodyTests(TestCase):

    def test_create_governing_body(self):
        boundary = Boundary.objects.create(name='Pennsylvania')
        boundary.save()
        governing_body = GoverningBody(name='Example Body', boundary=boundary)
        governing_body.save()

        self.assertIsInstance(governing_body, GoverningBody)


class PoliticalSubdivisionTests(TestCase):

    def test_political_subdivision_creation(self):
        boundary = Boundary.objects.create(name='Pennsylvania')
        boundary.save()
        governing_body = init_governing_body()
        governing_body.save()
        office = init_public_office()
        office.save()
        political_subdivision = init_political_subdivision()
        political_subdivision.save()

        self.assertEquals(political_subdivision.seats, 1)

    def test_seat_assignments(self):
        """
        Ensure the number of officials is not larger than a subdivision's number of seats.
        """
        political_subdivision = init_political_subdivision()
        political_subdivision.save()

        official1 = init_public_official()
        official1.save()
        official2 = init_public_official()
        official2.save()
        self.fail()


class PublicOfficialTests(TestCase):

    def test_public_official_creation(self):
        official = init_public_official()
        official.save()
        self.assertEquals(official.role, 'Legislator')

    def test_subdivision_assignment(self):
        political_subdivision = init_political_subdivision()
        political_subdivision.save()
        official = init_public_official()
        official.subdivision = political_subdivision
        official.save()

        self.assertEquals(official.subdivision, political_subdivision)


class SupportLevelTests(TestCase):

    def test_support_level_creation(self):
        campaign = init_campaign()
        official = init_public_official()
        support_level = SupportLevel.objects.create(campaign=campaign, official=official)
        support_level.save()
        self.assertIsInstance(support_level, SupportLevel)


class InterpersonalTieTests(TestCase):

    def test_interpersonal_tie_creation(self):
        official1 = init_public_official(first_name='Official', last_name='One')
        official2 = init_public_official(first_name='Official', last_name='Two')
        tie = InterpersonalTie.objects.create(official1=official1, official2=official2)
        tie.save()
        self.assertIsInstance(tie, InterpersonalTie)

    def test_interpersonal_tie_relationship_summary(self):
        official1 = init_public_official(first_name='Official', last_name='One')
        official2 = init_public_official(first_name='Official', last_name='Two')
        tie = InterpersonalTie.objects.create(official1=official1, official2=official2)
        tie.save()
        self.assertEquals(tie.relationship_summary(), 'Official One is unknown/neutral towards Official Two')

    def test_interpersonal_ties_to(self):
        official1 = init_public_official(first_name='Official', last_name='One')
        official2 = init_public_official(first_name='Official', last_name='Two')
        official3 = init_public_official(first_name='Official', last_name='Three')
        tie1 = InterpersonalTie.objects.create(official1=official1, official2=official2)
        tie1.save()
        tie2 = InterpersonalTie.objects.create(official1=official1, official2=official3)
        tie2.save()
        ties = official1.ties_from.all()
        self.assertIn(tie1, ties)
        self.assertIn(tie2, ties)

    def test_interpersonal_ties_from(self):
        official1 = init_public_official(first_name='Official', last_name='One')
        official2 = init_public_official(first_name='Official', last_name='Two')
        official3 = init_public_official(first_name='Official', last_name='Three')
        tie1 = InterpersonalTie.objects.create(official1=official1, official2=official3)
        tie1.save()
        tie2 = InterpersonalTie.objects.create(official1=official2, official2=official3)
        tie2.save()
        ties = official3.ties_to.all()
        self.assertIn(tie1, ties)
        self.assertIn(tie2, ties)


def init_political_party(name='Peace Party'):
    party = PoliticalParty.objects.create(name=name)

    return party


def init_governing_body():
    boundary = Boundary.objects.create(name='Pennsylvania')
    boundary.save()
    governing_body = GoverningBody(name='State Senate', boundary=boundary)
    governing_body.save()

    return governing_body


def init_political_subdivision(name='Test District'):
    office = init_public_office()
    subdivision = PoliticalSubdivision.objects.create(office=office, name=name)
    subdivision.save()

    return subdivision


def init_public_office(name='State Senator'):
    governing_body = init_governing_body()
    office = PublicOffice.objects.create(name=name, governing_body=governing_body)
    office.save()

    return office


def init_public_official(first_name='Jane', last_name='Doe'):
    party = init_political_party()
    office = init_public_office()
    subdivision = init_political_subdivision()
    official = PublicOfficial.objects.create(
        first_name=first_name,
        last_name=last_name,
        office=office,
        subdivision=subdivision,
        party=party
    )
    official.save()

    return official
