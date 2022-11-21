from django.test import TestCase

from accounts.models import Organization as OrgAccount
from core.models import GeographicBoundary, ContactInfo

from .models import (
    Organization,
    Person,
    Chapter,
    Platform,
    PlatformCategory,
    Campaign,
)


class OrganizationTests(TestCase):

    def test_organization_creation(self):
        organization = Organization(
            name='March on Harrisburg',
            url='https://www.mohpa.org'
        )
        organization.save()
        self.assertIsInstance(organization, Organization)


class PlatformTests(TestCase):

    def test_platform_creation(self):
        organization = init_organization()
        platform = Platform(title='Test Platform', organization=organization)
        platform.save()
        self.assertIsInstance(platform, Platform)


class PlatformCategoryTests(TestCase):

    def test_platform_category_creation(self):
        organization = init_organization()
        platform = Platform(title='Test Platform', organization=organization)
        platform.save()
        category = PlatformCategory(platform=platform, name='Category', order=1)
        category.save()
        self.assertIsInstance(category, PlatformCategory)


class CampaignTests(TestCase):

    def test_campaign_creation(self):
        organization = init_organization()
        platform = Platform(title='Test Platform', organization=organization)
        platform.save()
        campaign = Campaign(platform=platform, name='Campaign', status='brainstorming')
        campaign.save()
        self.assertIsInstance(campaign, Campaign)


class PersonTests(TestCase):

    def test_person_creation(self):
        organization = init_organization()
        contact = ContactInfo(first_name='Jane', last_name='Doe')
        contact.save()
        person = Person(organization=organization, contact=contact)
        person.save()
        self.assertIsInstance(person, Person)


class ChapterTests(TestCase):

    def test_chapter_creation(self):
        organization = init_organization()
        chapter = Chapter(name='Test Chapter', organization=organization)
        self.assertIsInstance(chapter,Chapter)


def init_organization():
    boundary = GeographicBoundary(name='Pennsylvania')
    boundary.save()
    org_contact = ContactInfo(first_name='Test', last_name='Contact')
    org_contact.save()
    organization = OrgAccount(
        name='March on Harrisburg',
        territory=boundary,
        primary_contact=org_contact
    )
    organization.save()

    return organization
