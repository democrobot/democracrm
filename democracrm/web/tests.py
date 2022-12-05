from django.test import TestCase

from .models import (Link, SocialMediaAccount)


class LinkTests(TestCase):

    def test_link_creation(self):
        link = Link(name='March on Harrisburg Website', url='https://www.mohpa.org')
        link.save()
        self.assertIsInstance(link, Link)
