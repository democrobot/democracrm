from django.contrib.gis.db import models

from core.models import CRMBase, CRMTreeBase
from places.models import Site


class Contact(CRMBase):
    """
    Contacts are records for an individual person that can be attached to a
    number of other models. When their information is updated, it's reflected
    anywhere their contact is linked to keep the information accurate.
    """

    # TODO: Ensure all relevant vCard fields can be imported/exported

    name_prefix = models.CharField(
        blank=True,
        max_length=50
    )
    first_name = models.CharField(
        max_length=100
    )
    middle_name = models.CharField(
        blank=True,
        max_length=100
    )
    last_name = models.CharField(
        max_length=100
    )
    name_suffix = models.CharField(
        blank=True,
        max_length=50
    )
    title = models.CharField(
        blank=True,
        max_length=255
    )
    personal_phone = models.CharField(
        blank=True,
        max_length=255
    )
    work_phone = models.CharField(
        blank=True,
        max_length=255
    )
    mobile_phone = models.CharField(
        blank=True,
        max_length=255
    )
    personal_fax = models.CharField(
        blank=True,
        max_length=255
    )
    work_fax = models.CharField(
        blank=True,
        max_length=255
    )
    personal_email = models.CharField(
        blank=True,
        max_length=255
    )
    work_email = models.CharField(
        blank=True,
        max_length=255
    )
    url = models.URLField(
        blank=True
    )
    birthday = models.DateField(
        null=True,
        blank=True
    )
    notes = models.TextField(
        blank=True
    )
    # If an address is needed, create and attach to a site
    site = models.ManyToManyField(
        Site,
        blank=True
    )

    # TODO: Implement vCard import/export and QR code generation
    # Might need a custom method on the manager for importing into a new Contact

    class Meta:
        verbose_name_plural = 'Contacts'

    def __str__(self):
        return self.full_name()

    def full_name(self):
        return f'{self.first_name} {self.last_name}'


class ContactRole(CRMBase):
    """
    Contact Roles are paired with Contacts when linked to other objects to
    provide a specific context to the person when linked to something else.
    """

    # TODO: Complete this model

    name = models.CharField(
        max_length=255
    )
    description = models.TextField(
        blank=True
    )

    class Meta:
        verbose_name_plural = 'Contact Roles'

    def __str__(self):
        return self.name


class ContactGroup(CRMTreeBase):
    """
    Contact Groups are used to organize Contacts. They can be nested to create
    hierarchical directories of contact information.
    """

    name = models.CharField(
        max_length=255
    )
    description = models.TextField(
        blank=True
    )
    # Explore ways to provide UI for this
    contacts = models.ManyToManyField(
        Contact,
        blank=True
    )

    class Meta:
        verbose_name_plural = 'Contact Groups'

    def __str__(self):
        return self.name
