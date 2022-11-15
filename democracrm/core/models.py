from django.db import models  # TODO: Migrate to GeoDjango models


class GeographicArea(models.Model):
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


class OrganizationAccount(models.Model):
    """
    Organizations represent the organizational account within the system; all
    management is based on this context by users. Organizations can choose to
    collaborate with others, share data, and track progress, but otherwise each
    organization's data is isolated to their own account.
    """
    name = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Organization Accounts'

    def __str__(self):
        return self.name


class ContactRole(models.Model):
    """

    """

    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Contact Roles"

    def __str__(self):
        return self.name


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


class Comment(models.Model):
    """
    Comments are text records that can be added to many other objects.
    """
    text = models.TextField()

