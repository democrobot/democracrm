from django.contrib.gis.db import models

from core.models import CRMBase


class Comment(CRMBase):
    """
    Comments are text records that can be added to many other objects.
    """
    text = models.TextField(blank=True)
