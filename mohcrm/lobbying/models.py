from django.db import models


class GoverningBody(models.Model):
    """
    A governing body is a level of government responsible for legislative,
    executive, and judicial authority for a defined geographic area containing
    one or more political subdivisions within it.

    Examples include federal, state, county, and municipal governments, each
    with specific governmental branches and/or offices.
    """
    name = models.CharField(null=False, max_length=255)
    # geom


class PoliticalSubdivision(models.Model):
    """
    A political subdivision is a specific part of a governing body, again with a
    defined geographic area coterminous or as a subset of the enclosing governing
    body. It is generally used to represent specific political districts and the
    seats included in that district.
    """

    name = models.CharField(null=False, max_length=255)
    district = models.IntegerField(null=True, blank=True)
    seats = models.IntegerField(default=1)
    # Needs geom field


class PublicOfficial(models.Model):
    """
    Represents elected or appointed public officials that are lobbying targets.
    """

    prefix_name = models.CharField(null=True, blank=True, max_length=50)
    first_name = models.CharField(null=False, max_length=100)
    middle_name = models.CharField(null=True, blank=True, max_length=100)
    last_name = models.CharField(null=False, max_length=100)
    suffix_name = models.CharField(null=True, blank=True, max_length=50)
    is_elected = models.BooleanField(default=True)
    official_type = models.CharField(null=False, max_length=100, default='Legislator')
    subdivision = models.ForeignKey(PoliticalSubdivision, on_delete=models.RESTRICT, null=True)



