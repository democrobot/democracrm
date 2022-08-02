from django.db import models  # TODO: Migrate to GeoDjango models


class Site(models.Model):
    """
    A Site is a point-based geospatial record.
    """
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    has_street_address = models.BooleanField(default=False)
    address_1 = models.CharField(max_length=255, blank=True)
    address_2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=255, blank=True)
    zip_code = models.CharField(max_length=10, blank=True)


class Location(models.Model):
    parent = models.ForeignKey('Location', on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
    description = models.TextField()


class Organization(models.Model):
    """

    """
    name = models.CharField(max_length=255)
    description = models.TextField()


class ContactInfo(models.Model):
    """

    """
    pass


class Note(models.Model):
    """

    """
    pass
