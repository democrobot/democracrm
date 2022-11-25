from django.db import models

from core.models import CRMBase
from places.models import Site


class ContactRole(CRMBase):
    """

    """

    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Contact Roles"

    def __str__(self):
        return self.name


class ContactInfo(CRMBase):
    """
    Contact info can be attached to a number of other models.
    """

    name_prefix = models.CharField(null=True, blank=True, max_length=50)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(null=True, blank=True, max_length=100)
    last_name = models.CharField(max_length=100)
    name_suffix = models.CharField(null=True, blank=True, max_length=50)
    title = models.CharField(null=True, blank=True, max_length=255)
    personal_phone = models.CharField(null=True, blank=True, max_length=255)
    work_phone = models.CharField(null=True, blank=True, max_length=255)
    mobile_phone = models.CharField(null=True, blank=True, max_length=255)
    personal_fax = models.CharField(null=True, blank=True, max_length=255)
    work_fax = models.CharField(null=True, blank=True, max_length=255)
    personal_email = models.CharField(null=True, blank=True, max_length=255)
    work_email = models.CharField(null=True, blank=True, max_length=255)
    description = models.TextField(null=True, blank=True)
    role = models.ForeignKey(ContactRole, null=True, blank=True, on_delete=models.PROTECT)

    # If an address is needed, create and attach to a site
    site = models.ManyToManyField(Site)

    class Meta:
        verbose_name_plural = "Contact Info"

    def __str__(self):
        return self.full_name()

    def full_name(self):
        return f'{self.first_name} {self.last_name}'


# TODO: Contact Groups?
