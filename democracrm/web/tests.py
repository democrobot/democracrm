from django.test import TestCase

from .models import (Link, SocialMediaAccount)


class LinkTests(TestCase):

    def test_link_creation(self):
        link = Link(name='March on Harrisburg Website', url='https://www.mohpa.org')
        link.save()
        self.assertIsInstance(link, Link)

    def test_url_responds(self):
        link = Link(name='March on Harrisburg Website', url='https://www.mohpa.org')
        link.save()
        self.assertTrue(link.url_responding())

    def test_url_does_not_respond(self):
        link = Link(name='March on Harrisburg Website', url='https://www.moohpaa.org')
        link.save()
        self.assertFalse(link.url_responding())
