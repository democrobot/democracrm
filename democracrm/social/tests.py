from django.test import TestCase

from .models import Comment


class CommentTests(TestCase):

    def test_note_creation(self):
        comment = Comment(text='This is a test.')
        comment.save()
        self.assertIsInstance(comment, Comment)
