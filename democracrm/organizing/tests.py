from django.test import TestCase

from accounts.models import Organization as OrgAccount
from core.models import GeographicBoundary, ContactInfo

from .models import (
    Organization,
    Member,
    Chapter,
    Platform,
    PlatformCategory,
    Campaign,
)


class OrganizationTests(TestCase):

    def test_organization_creation(self):
        organization = Organization(
            name='March on Harrisburg',
            url='https://www.mohpa.works'
        )
        organization.save()
        self.assertIsInstance(organization, Organization)


class PlatformTests(TestCase):

    def test_platform_creation(self):
        self.fail()


class PlatformCategoryTests(TestCase):

    def test_platform_category_creation(self):
        self.fail()


class CampaignTests(TestCase):

    def test_campaign_creation(self):
        self.fail()


class MemberTests(TestCase):

    def test_member_creation(self):
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
        contact = ContactInfo(first_name='Jane', last_name='Doe')
        contact.save()
        member = Member(organization=organization, contact=contact)
        member.save()
        self.assertIsInstance(member, Member)


class ChapterTests(TestCase):

    def test_chapter_creation(self):
        self.fail()
