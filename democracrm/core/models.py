import uuid

from django.db import models  # TODO: Migrate to GeoDjango models
from django.utils.html import format_html

import accounts.models


class CRMBase(models.Model):
    """
    Base model for all CRM models.
    """

    uuid = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)
    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    updated_on = models.DateTimeField(auto_now=True, editable=False)
    #TODO: fix object create/update
    #created_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, editable=False)
    #updated_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, editable=False)

    def update(self, update_dict=None, **kwargs):
        """ Helper method to update objects """
        if not update_dict:
            update_dict = kwargs
        update_fields = {'updated_on', 'updated_by'}
        for k, v in update_dict.items():
            setattr(self, k, v)
            update_fields.add(k)
        self.save(update_fields=update_fields)

    class Meta:
        abstract = True


class GeographicBoundary(CRMBase):
    """
    A geographic boundary is an official political boundary, represented by a
    polygon-based geospatial record that can be associated
    with a variety of other spatial overlays, such as governing bodies and
    political subdivisions.
    """

    # TODO: Define "root" of reform effort area, such as the state, and use that
    # to generate the base map. Only one record can be the root!

    # For now, boundaries can only have one parent, which is almost always true
    parent = models.ForeignKey(
        'GeographicBoundary',
        null=True,
        blank=True,
        on_delete=models.PROTECT
    )
    # Name should be the official name of the jurisdiction
    name = models.CharField(
        max_length=255
    )
    # Defined areas based off of this: https://www2.census.gov/geo/pdfs/reference/geodiagram.pdf
    # The focus is on areas with jurisdiction over elections
    LEVEL_CHOICES = (
        ('nation', 'Nation'),
        ('state', 'State'),
        ('county', 'County'),
        ('municipality', 'Municipality'),
    )
    level = models.CharField(
        max_length=255,
        choices=LEVEL_CHOICES,
    )

    class Meta:
        verbose_name_plural = "Geographic Boundaries"

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class GeographicRegion(CRMBase):
    """
    User-defined regions for use in organizations.
    """

    organization = models.ForeignKey('accounts.Organization', on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
    boundaries = models.ManyToManyField(GeographicBoundary)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Geographic Regions'


class Site(CRMBase):
    """
    A Site is a point-based geospatial record.
    """

    name = models.CharField(
        max_length=255
    )
    description = models.TextField(
        null=True,
        blank=True
    )
    # TODO: Add mailing address
    has_physical_address = models.BooleanField(
        default=False
    )
    physical_street_number = models.CharField(
        null=True,
        blank=True,
        max_length=10
    )
    physical_street_direction = models.CharField(null=True, blank=True, max_length=10)
    physical_street_name = models.CharField(null=True, blank=True, max_length=255)
    physical_street_suffix = models.CharField(null=True, blank=True, max_length=100)
    physical_unit_number = models.CharField(null=True, blank=True, max_length=50)
    physical_city = models.CharField(null=True, blank=True, max_length=255)
    physical_state = models.CharField(null=True, blank=True, max_length=255)
    physical_zip_code = models.CharField(null=True, blank=True, max_length=10)
    physical_county = models.CharField(null=True, blank=True, max_length=255)
    physical_latitude = models.FloatField(null=True, blank=True)
    physical_longitude = models.FloatField(null=True, blank=True)
    has_mailing_address = models.BooleanField(
        default=False
    )
    mailing_street_number = models.CharField(
        null=True,
        blank=True,
        max_length=10
    )
    mailing_street_direction = models.CharField(null=True, blank=True,
                                                 max_length=10)
    mailing_street_name = models.CharField(null=True, blank=True,
                                            max_length=255)
    mailing_street_suffix = models.CharField(null=True, blank=True,
                                              max_length=100)
    mailing_unit_number = models.CharField(null=True, blank=True,
                                            max_length=50)
    mailing_po_box = models.CharField(null=True, blank=True, max_length=255)
    mailing_city = models.CharField(null=True, blank=True, max_length=255)
    mailing_state = models.CharField(null=True, blank=True, max_length=255)
    mailing_zip_code = models.CharField(null=True, blank=True, max_length=10)
    mailing_county = models.CharField(null=True, blank=True, max_length=255)
    mailing_latitude = models.FloatField(null=True, blank=True)
    mailing_longitude = models.FloatField(null=True, blank=True)

    def full_physical_address(self):
        parts = []
        parts.append(self.physical_street_number)
        parts.append(self.physical_street_direction)
        parts.append(self.physical_street_name)
        parts.append(self.physical_street_suffix)
        parts.append(self.physical_unit_number)
        parts.append(self.physical_city)
        parts.append(self.physical_state)
        parts.append(self.physical_zip_code)
        return ' '.join([i for i in parts if i is not None])

    def full_mailing_address(self):
        parts = []
        parts.append(self.mailing_street_number)
        parts.append(self.mailing_street_direction)
        parts.append(self.mailing_street_name)
        parts.append(self.mailing_street_suffix)
        parts.append(self.mailing_unit_number)
        parts.append(self.mailing_po_box)
        parts.append(self.mailing_city)
        parts.append(self.mailing_state)
        parts.append(self.mailing_zip_code)
        return ' '.join([i for i in parts if i is not None])

    def physical_coordinates(self):
        return self.physical_latitude, self.physical_longitude

    def mailing_coordinates(self):
        return self.mailing_latitude, self.mailing_longitude

    def __str__(self):
        return self.name


class Location(CRMBase):
    """

    """

    parent = models.ForeignKey('Location', on_delete=models.PROTECT, blank=True, null=True)
    site = models.ForeignKey(Site, on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
    unit = models.CharField(null=True, blank=True, max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


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


class Comment(CRMBase):
    """
    Comments are text records that can be added to many other objects.
    """
    text = models.TextField()


class Link(CRMBase):
    """
    Links to online resources related to an object.
    """

    name = models.CharField(max_length=255)
    url = models.URLField()
    # Organizations that own links can mark them official
    is_official = models.BooleanField(default=False)


class SocialMediaAccount(CRMBase):
    """
    A social media account that should be tracked and/or engaged with.
    """

    PLATFORMS = (
        ('twitter', 'Twitter'),
        ('instagram', 'Instagram'),
        ('facebook', 'Facebook'),
        ('linkedin', 'LinkedIn'),
    )
    platform = models.CharField(null=False, max_length=255, choices=PLATFORMS)
    handle = models.CharField(null=False, blank=False, max_length=255)
    voter = models.ForeignKey('lobbying.Voter', null=True, blank=True, on_delete=models.RESTRICT)

    class Meta:
        verbose_name_plural = "Social Media Accounts"

    def __repr__(self):
        return self.handle

    def __str__(self):
        return f'@{self.handle}'

    def url(self):
        if self.platform == 'twitter':
            url_text = f'https://www.twitter.com/{self.handle}'
            return format_html('<a href="{url}">{url}</a>', url=url_text)
        elif self.platform == 'instagram':
            url_text = f'https://www.instagram.com/{self.handle}'
            return format_html('<a href="{url}">{url}</a>', url=url_text)
        elif self.platform == 'facebook':
            url_text = f'https://www.facebook.com/{self.handle}'
            return format_html('<a href="{url}">{url}</a>', url=url_text)
        elif self.platform == 'linkedin':
            url_text = f'https://www.linkedin.com/in/{self.handle}'
            return format_html('<a href="{url}">{url}</a>', url=url_text)
        else:
            return 'N/A'
