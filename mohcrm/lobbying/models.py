from django.db import models


class GoverningBody(models.Model):
    name = models.CharField(null=False, max_length=255)


class PoliticalSubdivision(models.Model):
    name = models.CharField(null=False, max_length=255)
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



