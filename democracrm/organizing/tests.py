from django.test import TestCase

from accounts.models import OrganizationAccount
from accounts.tests import init_user_account
from contacts.models import Contact
from places.models import Boundary


from .models import (
    Organization,
    Person,
    Chapter,
    CampaignCategory,
    Campaign,
)


class OrganizationTests(TestCase):

    def test_organization_creation(self):
        org_account = init_org_account()
        organization = Organization(
            org_account=org_account,
            name='March on Harrisburg',
            url='https://www.mohpa.org'
        )
        organization.save()
        self.assertIsInstance(organization, Organization)


class CampaignCategoryTests(TestCase):

    def test_platform_category_creation(self):
        org_account = init_org_account()
        category = CampaignCategory(org_account=org_account, name='Category', order=1)
        category.save()
        self.assertIsInstance(category, CampaignCategory)


class CampaignTests(TestCase):

    def test_campaign_creation(self):
        org_account = init_org_account()
        campaign = Campaign(org_account=org_account, name='Campaign', status='brainstorming')
        campaign.save()
        self.assertIsInstance(campaign, Campaign)


class PersonTests(TestCase):

    def test_person_creation(self):
        user_account = init_user_account()
        org_account = init_org_account()
        contact = Contact(first_name='Jane', last_name='Doe')
        contact.save()
        person = Person(user_account=user_account, org_account=org_account, contact=contact)
        person.save()
        self.assertIsInstance(person, Person)


class ChapterTests(TestCase):

    def test_chapter_creation(self):
        user_account = init_user_account()
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


def init_campaign():
    org_account = init_org_account()
    campaign = Campaign.objects.create(name='Test Campaign', org_account=org_account)
    campaign.save()

    return campaign
