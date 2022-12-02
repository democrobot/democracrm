from django.test import TestCase

from accounts.models import OrganizationAccount
from contacts.models import Contact
from places.models import Boundary


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
        org_account = init_org_account()
        platform = Platform(title='Test Platform', org_account=org_account)
        platform.save()
        self.assertIsInstance(platform, Platform)


class PlatformCategoryTests(TestCase):

    def test_platform_category_creation(self):
        org_account = init_org_account()
        platform = Platform(title='Test Platform', org_account=org_account)
        platform.save()
        category = PlatformCategory(platform=platform, name='Category', order=1)
        category.save()
        self.assertIsInstance(category, PlatformCategory)


class CampaignTests(TestCase):

    def test_campaign_creation(self):
        org_account = init_org_account()
        platform = Platform(title='Test Platform', org_account=org_account)
        platform.save()
        campaign = Campaign(platform=platform, name='Campaign', status='brainstorming')
        campaign.save()
        self.assertIsInstance(campaign, Campaign)


class PersonTests(TestCase):

    def test_person_creation(self):
        org_account = init_org_account()
        contact = Contact(first_name='Jane', last_name='Doe')
        contact.save()
        person = Person(org_account=org_account, contact=contact)
        person.save()
        self.assertIsInstance(person, Person)


class ChapterTests(TestCase):

    def test_chapter_creation(self):
        org_account = init_org_account()
        chapter = Chapter(name='Test Chapter', org_account=org_account)
        self.assertIsInstance(chapter, Chapter)


def init_org_account():
    boundary = Boundary(name='Pennsylvania')
    boundary.save()
    org_contact = Contact(first_name='Test', last_name='Contact')
    org_contact.save()
    org_account = OrganizationAccount(
        name='March on Harrisburg',
        territory=boundary,
        #primary_contact=org_contact
    )
    org_account.save()

    return org_account


def init_platform():
    org_account = init_org_account()
    platform = Platform(title='Test Platform', org_account=org_account)
    platform.save()

    return platform


def init_campaign():
    platform = init_platform()
    campaign = Campaign(name='Test Campaign', platform=platform)
    campaign.save()

    return campaign
