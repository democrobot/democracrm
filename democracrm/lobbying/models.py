import uuid
from django.db import models

from core.models import CRMBase
from organizing.models import Campaign

class PoliticalParty(models.Model):
    """
    A formal political party active with candidates and/or elected officials
    being represented.
    """

    name = models.CharField(null=False, max_length=255)

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Political Parties"


class Voter(models.Model):
    """
    An individual voter record.
    """

    uuid = models.UUIDField('UUID', default=uuid.uuid4)
    party = models.ForeignKey(PoliticalParty, on_delete=models.RESTRICT)
    first_name = models.CharField('First Name', null=True, blank=True, max_length=255)
    middle_name = models.CharField('Middle Name', null=True, blank=True, max_length=255)
    last_name = models.CharField('Last Name', null=True, blank=True, max_length=255)
    sex = models.CharField('Sex', null=True, blank=True, max_length=10)
    birth_date = models.DateField('Birth Date', blank=True)
    initial_registration = models.DateField('Initial Registration', blank=True)
    current_registration = models.DateField('Current Registration', blank=True)
    address_number = models.CharField('Address Number', null=True, blank=True, max_length=100)
    address_street_direction = models.CharField('Address Street Direction', null=True, blank=True, max_length=100)
    address_street_name = models.CharField('Address Street Name', null=True, blank=True, max_length=100)
    address_street_type = models.CharField('Address Street Type', null=True, blank=True, max_length=100)
    address_unit = models.CharField('Address Unit', null=True, blank=True, max_length=100)
    city = models.CharField('City', null=True, blank=True, max_length=100)
    state = models.CharField('State', null=True, blank=True, max_length=100)
    zip_code = models.CharField('ZIP Code', null=True, blank=True, max_length=100)
    phone_number = models.CharField('Phone Number', null=True, blank=True, max_length=11)
    email_address = models.CharField('Email', null=True, blank=True, max_length=254)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def full_name(self):
        if self.first_name and self.last_name:
            return str(self)
        else:
            return 'N/A'


class GoverningBody(models.Model):
    """
    A governing body is a level of government responsible for legislative,
    executive, and judicial authority for a defined geographic area containing
    one or more political subdivisions within it.

    Examples include federal, state, county, and municipal governments, each
    with specific governmental branches and/or offices.
    """

    name = models.CharField(null=False, max_length=255)
    LEVEL_CHOICES = (
        ('federal', 'Federal'),
        ('state', 'State'),
        ('county', 'County'),
        ('municipal', 'Municipal'),
    )
    level = models.CharField(max_length=255, choices=LEVEL_CHOICES)
    boundary = models.ForeignKey('core.GeographicBoundary', on_delete=models.RESTRICT)
    # geom

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Governing Bodies"

    def __str__(self):
        return self.name


class PublicOffice(models.Model):
    """
    Represents the office that public officials serve within a governing body.
    """

    TYPE_CHOICES = (
        ('legislative', 'Legislative'),
        ('executive', 'Executive'),
        ('judicial', 'Judicial'),
        ('other', 'Other'),
    )
    type = models.CharField(default='legislative', max_length=255, choices=TYPE_CHOICES)
    governing_body = models.ForeignKey(GoverningBody, on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
    seats = models.IntegerField(default=1)

    class Meta:
        verbose_name_plural = 'Public Offices'

    def __str__(self):
        return self.name

    def officials_count(self):
        return len(self.publicofficial_set.all())


class PoliticalSubdivision(models.Model):
    """
    A political subdivision is a defined subset of a public office, again with a
    defined geographic area coterminous or as a subset of the public office.
    It is generally used to represent specific political districts and the
    seats included in that district.
    """

    office = models.ForeignKey(PublicOffice, null=True, on_delete=models.PROTECT)
    name = models.CharField(null=False, max_length=255)
    district = models.IntegerField(null=True, blank=True)
    seats = models.IntegerField(default=1)
    # Needs geom field

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Political Subdivisions"

    def __repr__(self):
        return f'{self.name} ({self.office.governing_body})'

    def __str__(self):
        return f'{self.name} ({self.office.governing_body})'

    def governing_body(self):
        return self.office.governing_body


class PublicOfficial(models.Model):
    """
    Represents elected or appointed public officials that are lobbying targets.
    """

    office = models.ForeignKey(PublicOffice, null=True, blank=True, on_delete=models.RESTRICT)
    is_elected = models.BooleanField(default=True)
    title = models.CharField(default='Legislator', max_length=255)
    is_leadership = models.BooleanField(default=False)
    leadership_title = models.CharField(null=True, blank=True, max_length=255)
    prefix_name = models.CharField(null=True, blank=True, max_length=50)
    first_name = models.CharField(null=False, max_length=100)
    middle_name = models.CharField(null=True, blank=True, max_length=100)
    last_name = models.CharField(null=False, max_length=100)
    suffix_name = models.CharField(null=True, blank=True, max_length=50)
    party = models.ForeignKey(PoliticalParty, null=True, blank=True, on_delete=models.PROTECT)
    service_start = models.DateField(null=True, blank=True)
    service_end = models.DateField(null=True, blank=True)
    ROLE_CHOICES = (
        ('legislative', 'Legislative'),
        ('executive', 'Executive'),
        ('judicial', 'Judicial'),
        ('administrative', 'Administrative'),
        ('clerical', 'Clerical'),
    )
    role = models.CharField(null=False, max_length=100, choices=ROLE_CHOICES, default='Legislator')
    subdivision = models.ForeignKey(PoliticalSubdivision, on_delete=models.RESTRICT, null=True)
    notes = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Public Officials"

    def __str__(self):
        return self.full_name()

    def full_name(self):
        return f'{self.first_name} {self.last_name}'


class Committee(models.Model):
    """
    Represents committees, commissions, or other bodies that review legislation
    before releasing it for final passage.
    """

    name = models.CharField(max_length=255)
    body = models.ForeignKey(GoverningBody, null=True, blank=True, on_delete=models.RESTRICT)
    office = models.ForeignKey(PublicOffice, on_delete=models.RESTRICT)

    def __str__(self):
        return self.name


class Session(models.Model):
    """
    Represents legislative sessions, within which bills exist and must be enacted
    before the session ends and the legislative process restarts.
    """

    # TODO: Can this be automated for each defined governing body's
    #  legislative branch?

    body = models.ForeignKey(GoverningBody, on_delete=models.RESTRICT)
    name = models.CharField(null=True, blank=True, max_length=255) # TODO: Set based on duration field
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)


class Legislation(models.Model):
    """
    Represents proposed or existing legislation related to campaigns.
    """

    name = models.CharField(max_length=255)
    body = models.ForeignKey(GoverningBody, on_delete=models.RESTRICT)
    committee = models.ForeignKey(Committee, null=True, blank=True, on_delete=models.RESTRICT)
    session = models.ForeignKey(Session, null=True, blank=True, on_delete=models.RESTRICT)
    number = models.CharField(null=True, blank=True, max_length=255)
    description = models.TextField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    STATUS_CHOICES = (
        ('proposed', 'Proposed'),
        ('in-committee', 'In Committee'),
        ('in-debate', 'In Debate'),
        ('voting-on', 'Voting On'),
        ('adopted', 'Adopted'),
        ('rejected', 'Rejected'),
    )
    status = models.CharField(null=True, blank=True, max_length=255, choices=STATUS_CHOICES)
    campaign = models.ForeignKey('organizing.Campaign', on_delete=models.RESTRICT)

    class Meta:
        verbose_name_plural = 'Legislation'

    def __str__(self):
        return self.name


class SupportLevel(CRMBase):
    """
    SupportLevel models the level of support of an individual public official for
    a special campaign and associated legislation.
    """

    official = models.ForeignKey(PublicOfficial, on_delete=models.PROTECT)
    SUPPORT_LEVEL_CHOICES = (
        ('strongly_supports', 'Strongly Supports'),
        ('supports', 'Supports'),
        ('undecided', 'Undecided'),
        ('opposes', 'Opposes'),
        ('strongly_opposes', 'Strongly Opposes'),
    )
    campaign = models.ForeignKey(Campaign, on_delete=models.PROTECT)
    campaign_support = models.CharField(max_length=255, choices=SUPPORT_LEVEL_CHOICES)
    legislation = models.ForeignKey(Legislation, null=True, blank=True, on_delete=models.PROTECT)
    legislation_support = models.CharField(max_length=255, choices=SUPPORT_LEVEL_CHOICES)

    class Meta:
        verbose_name_plural = 'Support Levels'

    def __str__(self):
        return f'{self.official} on {self.campaign}'
