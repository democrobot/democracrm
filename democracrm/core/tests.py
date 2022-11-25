from django.test import TestCase

from .models import (Comment, Link)


class CommentTests(TestCase):

    def test_note_creation(self):
        comment = Comment(text='This is a test.')
        comment.save()
        self.assertIsInstance(comment, Comment)


class LinkTests(TestCase):

    def test_link_creation(self):
        link = Link(name='March on Harrisburg Website', url='https://www.mohpa.org')
        link.save()
        self.assertIsInstance(link, Link)
