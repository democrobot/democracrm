import uuid

from django.db import models  # TODO: Migrate to GeoDjango models


class CRMBase(models.Model):
    """
    Base model for all CRM models.
    """

    uuid = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def update(self, update_dict=None, **kwargs):
        """ Helper method to update objects """
        if not update_dict:
            update_dict = kwargs
        update_fields = {"updated_on"}
        for k, v in update_dict.items():
            setattr(self, k, v)
            update_fields.add(k)
        self.save(update_fields=update_fields)

    class Meta:
        abstract = True


class GeographicArea(CRMBase):
    """
    A Geographic Area is a polygon-based geospatial record that can be associated
    with a variety of other spatial overlays, such as governing bodies and
    political subdivisions. Areas should be those that are generally addressable.
    """

    # TODO: Define "root" of reform effort area, such as the state, and use that
    # to generate the base map. Only one record can be the root!

    parent = models.ForeignKey('GeographicArea', null=True, blank=True, on_delete=models.RESTRICT)
    name = models.CharField(max_length=255)
    # Defined areas based off of this: https://www2.census.gov/geo/pdfs/reference/geodiagram.pdf
    # The focus is on areas with jurisdiction over elections
    LEVEL_CHOICES = (
        ('nation', 'Nation'),
        ('state', 'State'),
        ('county', 'County'),
        ('municipality', 'Municipality'),
    )
    level = models.CharField(null=True, blank=True, max_length=255, choices=LEVEL_CHOICES)

    class Meta:
        verbose_name_plural = "Geographic Areas"

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class Site(CRMBase):
    """
    A Site is a point-based geospatial record.
    """

    name = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    has_street_address = models.BooleanField(default=False)
    street_number = models.CharField(max_length=10, blank=True)
    street_direction = models.CharField(max_length=10, blank=True)
    street_name = models.CharField(max_length=255, blank=True)
    street_suffix = models.CharField(max_length=100, blank=True)
    unit_number = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=255, blank=True)
    zip_code = models.CharField(max_length=10, blank=True)
    county = models.CharField(max_length=255, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)


class Location(CRMBase):
    """

    """
    parent = models.ForeignKey('Location', on_delete=models.PROTECT, blank=True, null=True)
    site = models.ForeignKey(Site, on_delete=models.PROTECT)
    name = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)


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

    name_prefix = models.CharField(max_length=50, blank=True)
    first_name = models.CharField(max_length=100, blank=True)
    middle_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    name_suffix = models.CharField(max_length=50, blank=True)
    title = models.CharField(max_length=255, blank=True)
    personal_phone = models.CharField(max_length=15, blank=True)
    work_phone = models.CharField(max_length=15, blank=True)
    personal_email = models.CharField(max_length=255, blank=True)
    work_email = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    role = models.ForeignKey(ContactRole, null=True, blank=True, on_delete=models.RESTRICT)

    # If an address is needed, create and attach to a site
    site = models.ForeignKey(Site, on_delete=models.CASCADE, blank=True, null=True)

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

