from django.test import TestCase

from .models import GoverningBody, PoliticalSubdivision, PublicOfficial


class GoverningBodyTests(TestCase):

    def test_create_governing_body(self):
        governing_body = GoverningBody(name='Example Body')
        governing_body.save()


class PoliticalSubdivisionTests(TestCase):

    def test_political_subdivision_creation(self):
        political_subdivision = PoliticalSubdivision()
        political_subdivision.save()

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
        self.assertEquals(official.official_type, 'Legislator')

    def test_subdivision_assignment(self):
        political_subdivision = PoliticalSubdivision(name='Example District')
        political_subdivision.save()
        official = PublicOfficial(first_name='Jane', last_name='Doe', subdivision=political_subdivision)
        official.save()

        self.assertEquals(official.subdivision, political_subdivision)