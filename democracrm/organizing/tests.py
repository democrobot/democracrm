from django.test import TestCase

from accounts.models import OrganizationAccount
from accounts.tests import init_user_account
from contacts.models import Contact
from places.models import Boundary


from .models import (
    OrganizationGroup,
    Organization,
    PersonGroup,
    Person,
    Chapter,
    CampaignCategory,
    Campaign,
    Relationship,
)


class OrganizationTests(TestCase):

    def test_organization_group_creation(self):
        org_account = init_org_account()
        org_group = OrganizationGroup.objects.create(
            org_account=org_account,
            name = 'Test Group',
            description='A test org. group'
        )
        org_group.save()
        self.assertIsInstance(org_group, OrganizationGroup)

    def test_organization_creation(self):
        org_account = init_org_account()
        organization = Organization.objects.create(
            org_account=org_account,
            name='March on Harrisburg',
            url='https://www.mohpa.org'
        )
        organization.save()
        self.assertIsInstance(organization, Organization)


class CampaignCategoryTests(TestCase):

    def test_platform_category_creation(self):
        org_account = init_org_account()
        category = CampaignCategory.objects.create(org_account=org_account, name='Category', order=1)
        category.save()
        self.assertIsInstance(category, CampaignCategory)


class CampaignTests(TestCase):

    def test_campaign_creation(self):
        org_account = init_org_account()
        campaign = Campaign.objects.create(org_account=org_account, name='Campaign', status='brainstorming')
        campaign.save()
        self.assertIsInstance(campaign, Campaign)


class PersonTests(TestCase):

    def test_person_group_creation(self):
        self.fail()

    def test_person_creation(self):
        user_account = init_user_account()
        org_account = init_org_account()
        contact = Contact.objects.create(first_name='Jane', last_name='Doe')
        contact.save()
        person = Person.objects.create(user_account=user_account, org_account=org_account, contact=contact)
        person.save()
        self.assertIsInstance(person, Person)


class ChapterTests(TestCase):

    def test_chapter_creation(self):
        user_account = init_user_account()
        org_account = init_org_account()
        chapter = Chapter.objects.create(name='Test Chapter', org_account=org_account)
        self.assertIsInstance(chapter, Chapter)


class RelationshipTests(TestCase):

    def test_relationship_creation(self):
        org_account = init_org_account()
        contact = Contact.objects.create(first_name='Jane', last_name='Doe')
        person = Person.objects.create(org_account=org_account, contact=contact)
        organization = Organization.objects.create(
            org_account=org_account,
            name='March on Harrisburg'
        )
        relationship = Relationship.objects.create(person1=person, organization2=organization, type='Member of')
        relationship.outgoing_field = 'person1'
        relationship.incoming_field = 'organization2'
        relationship.save()
        print(person.outgoing_relations.all())
        print(organization.incoming_relations.all())


def init_org_account():
    boundary = Boundary.objects.create(name='Pennsylvania')
    boundary.save()
    org_contact = Contact.objects.create(first_name='Test', last_name='Contact')
    org_contact.save()
    org_account = OrganizationAccount.objects.create(
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
