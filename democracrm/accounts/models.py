from django.contrib.auth.models import AbstractUser
from django.db import models  # TODO: Migrate to GeoDjango models

from .managers import UserManager
from core.models import CRMBase


class User(AbstractUser, CRMBase):
    email = models.EmailField(unique=True)
    username = None  # disable the AbstractUser.username field
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()


class Organization(CRMBase):
    """
    Organizations represent the organizational account within the system; all
    management is based on this context by users. Organizations can choose to
    collaborate with others, share data, and track progress, but otherwise each
    organization's data is isolated to their own account.
    """
    name = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    territory = models.ForeignKey('core.GeographicArea', on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = 'Organizations'

    def __str__(self):
        return self.name
