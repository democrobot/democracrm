from django.contrib.auth.models import AbstractUser
from django.db import models  # TODO: Migrate to GeoDjango models

from .managers import UserManager
from core.models import CRMBase
from places.models import Boundary
from contacts.models import ContactInfo


class UserAccount(AbstractUser, CRMBase):
    """
    User accounts within the platform. Users remain independent of organizations,
    so that they can work with multiple organizations. However, objects created
    in the context of an organization become owned by that organization, and
    while key objects can be created and edited by users, deletion is more
    restricted.
    """

    email = models.EmailField(unique=True)
    username = None  # disable the AbstractUser.username field
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name_plural = 'User Accounts'


class OrganizationAccount(CRMBase):
    """
    Organizations represent the organizational account within the system; all
    management is based on this context by users. Organizations can choose to
    collaborate with others, share data, and track progress, but otherwise each
    organization's data is isolated to their own account.
    """

    name = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(blank=True)
    territory = models.ForeignKey(Boundary, on_delete=models.PROTECT)
    # Creating a primary contact is mandatory for creating an organization and
    # this information will be published publicly
    primary_contact = models.ForeignKey(ContactInfo, on_delete=models.PROTECT)
    notes = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Organization Accounts'

    def __str__(self):
        return self.name
