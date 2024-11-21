from django.test import TestCase

from organizing.tests import init_campaign
from places.models import Boundary
from places.tests import init_boundary


from .models import (
    Committee,
    GoverningBody,
    InterpersonalTie,
    Legislation,
    LegislationGroup,
    LegislativeSession,
    PoliticalParty,
    PoliticalSubdivision,
    PublicOffice,
    PublicOfficial,
    PublicOfficialPosition,
    PublicOfficialGroup,
    SupportLevel,
    Voter
)


class GoverningBodyTests(TestCase):

    def test_create_governing_body(self):
        boundary = Boundary.objects.create(name='Pennsylvania', level='state')
        boundary.save()
        governing_body = GoverningBody(name='Example Body', boundary=boundary)
        governing_body.save()

        self.assertIsInstance(governing_body, GoverningBody)


class PoliticalSubdivisionTests(TestCase):

    def test_political_subdivision_creation(self):
        boundary = Boundary.objects.create(name='Pennsylvania', level='state')
        boundary.save()
        governing_body = init_governing_body()
        governing_body.save()
        public_office = init_public_office()
        public_office.save()
        political_subdivision = init_political_subdivision()
        political_subdivision.save()

        self.assertEqual(political_subdivision.seats, 1)

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


class PublicOfficialPositionTests(TestCase):

    def test_public_official_position_creation(self):
        official_position = init_public_official()
        official_position.save()
        self.assertEqual(official_position.role, PublicOfficial.Role.LEGISLATIVE)

    def test_subdivision_assignment(self):
        political_subdivision = init_political_subdivision()
        political_subdivision.save()
        official = init_public_official()
        official.subdivision = political_subdivision
        official.save()

        self.assertEqual(official.subdivision, political_subdivision)


class PublicOfficialTests(TestCase):

    def test_public_official_creation(self):
        official = init_public_official()
        official.save()
        self.assertEqual(official.role, PublicOfficial.Role.LEGISLATIVE)

    def test_subdivision_assignment(self):
        political_subdivision = init_political_subdivision()
        political_subdivision.save()
        official = init_public_official()
        official.subdivision = political_subdivision
        official.save()

        self.assertEqual(official.subdivision, political_subdivision)





class SupportLevelTests(TestCase):

    def test_support_level_creation(self):
        campaign = init_campaign()
        public_official = init_public_official()
        support_level = SupportLevel.objects.create(campaign=campaign, public_official=public_official)
        support_level.save()
        self.assertIsInstance(support_level, SupportLevel)


class InterpersonalTieTests(TestCase):

    def test_interpersonal_tie_creation(self):
        public_official1 = init_public_official(first_name='Official', last_name='One')
        public_official2 = init_public_official(first_name='Official', last_name='Two')
        tie = InterpersonalTie.objects.create(public_official1=public_official1, public_official2=public_official2)
        tie.save()
        self.assertIsInstance(tie, InterpersonalTie)

    def test_interpersonal_tie_relationship_summary(self):
        public_official1 = init_public_official(first_name='Official', last_name='One')
        public_official2 = init_public_official(first_name='Official', last_name='Two')
        tie = InterpersonalTie.objects.create(public_official1=public_official1, public_official2=public_official2)
        tie.save()
        self.assertEqual(tie.relationship_summary(), 'Official One is unknown/neutral towards Official Two')

    def test_interpersonal_ties_to(self):
        public_official1 = init_public_official(first_name='Official', last_name='One')
        public_official2 = init_public_official(first_name='Official', last_name='Two')
        public_official3 = init_public_official(first_name='Official', last_name='Three')
        tie1 = InterpersonalTie.objects.create(public_official1=public_official1, public_official2=public_official2)
        tie1.save()
        tie2 = InterpersonalTie.objects.create(public_official1=public_official1, public_official2=public_official3)
        tie2.save()
        ties = public_official1.ties_from.all()
        self.assertIn(tie1, ties)
        self.assertIn(tie2, ties)

    def test_interpersonal_ties_from(self):
        public_official1 = init_public_official(first_name='Official', last_name='One')
        public_official2 = init_public_official(first_name='Official', last_name='Two')
        public_official3 = init_public_official(first_name='Official', last_name='Three')
        tie1 = InterpersonalTie.objects.create(public_official1=public_official1, public_official2=public_official3)
        tie1.save()
        tie2 = InterpersonalTie.objects.create(public_official1=public_official2, public_official2=public_official3)
        tie2.save()
        ties = public_official3.ties_to.all()
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
    boundary = init_boundary()
    public_office = init_public_office()
    political_subdivision = PoliticalSubdivision.objects.create(
        boundary=boundary,
        public_office=public_office,
        name=name
    )
    political_subdivision.save()

    return political_subdivision


def init_public_office(name='State Senator'):
    governing_body = init_governing_body()
    public_office = PublicOffice.objects.create(name=name, governing_body=governing_body)
    public_office.save()

    return public_office


def init_public_official(first_name='Jane', last_name='Doe'):
    political_party = init_political_party()
    public_office = init_public_office()
    political_subdivision = init_political_subdivision()
    public_official = PublicOfficial.objects.create(
        first_name=first_name,
        last_name=last_name,
        public_office=public_office,
        political_subdivision=political_subdivision,
        political_party=political_party
    )
    public_official.save()

    return public_official
