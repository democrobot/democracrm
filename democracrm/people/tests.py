from django.test import TestCase

from .models import Contact, ContactRole, ContactGroup


class ContactTests(TestCase):

    def test_contact_creation(self):
        contact = Contact.objects.create(first_name='Jane', last_name='Doe')
        contact.save()
        self.assertIsInstance(contact, Contact)

    def test_contact_full_name(self):
        first_name = 'Jane'
        last_name = 'Doe'
        contact = Contact.objects.create(first_name=first_name, last_name=last_name)
        contact.save()
        self.assertEquals(contact.full_name(), f'{first_name} {last_name}')


class ContactRoleTests(TestCase):

    def test_contact_role_creation(self):
        contact_role = ContactRole.objects.create(name='Test Role')
        contact_role.save()
        self.assertIsInstance(contact_role, ContactRole)

    def test_contact_creation(self):
        contact = Contact.objects.create(first_name='Jane', last_name='Doe')
        contact.save()
        contact_role = ContactRole.objects.create(name='Test Role')
        contact_role.save()
        self.fail('Finish this test!')


class ContactGroupTests(TestCase):

    def test_contact_group_creation(self):
        contact_group = ContactGroup.objects.create(name='Test Group')
        contact_group.save()
        self.assertIsInstance(contact_group, ContactGroup)

    def test_contact_group_addition(self):
        contact = Contact.objects.create(first_name='Jane', last_name='Doe')
        contact.save()
        contact_group = ContactGroup.objects.create(name='Test Group')
        contact_group.save()
        contact_group.contacts.add(contact)
        self.assertIn(contact, contact_group.contacts.all())
