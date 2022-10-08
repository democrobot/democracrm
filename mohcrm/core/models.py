from django.db import models  # TODO: Migrate to GeoDjango models


class Site(models.Model):
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


class Location(models.Model):
    """

    """
    parent = models.ForeignKey('Location', on_delete=models.PROTECT, blank=True, null=True)
    site = models.ForeignKey(Site, on_delete=models.PROTECT)
    name = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)


class Organization(models.Model):
    """

    """
    name = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)


class ContactInfo(models.Model):
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

    # If an address is needed, create a site
    site = models.ForeignKey(Site, on_delete=models.CASCADE, blank=True, null=True)


class Note(models.Model):
    """
    Notes are text records that can be added to many other objects.
    """
    pass
