import uuid
from django.db import models

from core.models import CRMBase
from organizing.models import Campaign


class PoliticalParty(CRMBase):
    """
    A formal political party active with candidates and/or elected officials
    being represented.
    """

    name = models.CharField(max_length=255)
    # TODO: Should parties be linked to boundaries?
    # TODO: Should they be hierarchical?

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Political Parties"


class Voter(CRMBase):
    """
    An individual voter record.
    """

    party = models.ForeignKey(PoliticalParty, on_delete=models.RESTRICT)
    first_name = models.CharField('First Name', blank=True, max_length=255)
    middle_name = models.CharField('Middle Name', blank=True, max_length=255)
    last_name = models.CharField('Last Name', blank=True, max_length=255)
    sex = models.CharField('Sex', blank=True, max_length=10)
    birth_date = models.DateField('Birth Date', blank=True)
    initial_registration = models.DateField('Initial Registration', blank=True)
    current_registration = models.DateField('Current Registration', blank=True)
    address_number = models.CharField('Address Number', blank=True, max_length=100)
    address_street_direction = models.CharField('Address Street Direction', blank=True, max_length=100)
    address_street_name = models.CharField('Address Street Name', blank=True, max_length=100)
    address_street_type = models.CharField('Address Street Type', blank=True, max_length=100)
    address_unit = models.CharField('Address Unit', blank=True, max_length=100)
    city = models.CharField('City', blank=True, max_length=100)
    state = models.CharField('State', blank=True, max_length=100)
    zip_code = models.CharField('ZIP Code', blank=True, max_length=100)
    phone_number = models.CharField('Phone Number', blank=True, max_length=11)
    email_address = models.CharField('Email', blank=True, max_length=254)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def full_name(self):
        if self.first_name and self.last_name:
            return str(self)
        else:
            return 'N/A'


class GoverningBody(CRMBase):
    """
    A governing body is a level of government responsible for legislative,
    executive, and judicial authority for a defined geographic area containing
    one or more political subdivisions within it.

    Examples include federal, state, county, and municipal governments, each
    with specific governmental branches and/or offices.
    """

    name = models.CharField(max_length=255)
    LEVEL_CHOICES = (
        ('federal', 'Federal'),
        ('state', 'State'),
        ('county', 'County'),
        ('municipal', 'Municipal'),
    )
    level = models.CharField(max_length=255, choices=LEVEL_CHOICES)
    boundary = models.ForeignKey('places.Boundary', on_delete=models.RESTRICT)
    # geom

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Governing Bodies"

    def __str__(self):
        return self.name


class PublicOffice(CRMBase):
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


class PoliticalSubdivision(CRMBase):
    """
    A political subdivision is a defined subset of a public office, again with a
    defined geographic area coterminous or as a subset of the public office.
    It is generally used to represent specific political districts and the
    seats included in that district.
    """

    office = models.ForeignKey(PublicOffice, on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
    district = models.IntegerField(null=True, blank=True)
    seats = models.IntegerField(default=1)
    # Needs boundary field

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Political Subdivisions"

    def __repr__(self):
        return f'{self.name} ({self.office.governing_body})'

    def __str__(self):
        return f'{self.name} ({self.office.governing_body})'

    def governing_body(self):
        return self.office.governing_body


class PublicOfficial(CRMBase):
    """
    Represents elected or appointed public officials that are lobbying targets.
    """

    office = models.ForeignKey(PublicOffice, blank=True, on_delete=models.RESTRICT)
    is_elected = models.BooleanField(default=True)
    title = models.CharField(default='Legislator', max_length=255)
    is_leadership = models.BooleanField(default=False)
    leadership_title = models.CharField(blank=True, max_length=255)
    prefix_name = models.CharField(blank=True, max_length=50)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(blank=True, max_length=100)
    last_name = models.CharField(max_length=100)
    suffix_name = models.CharField(blank=True, max_length=50)
    party = models.ForeignKey(PoliticalParty, blank=True, on_delete=models.PROTECT)
    service_start = models.DateField(null=True, blank=True)
    service_end = models.DateField(null=True, blank=True)
    ROLE_CHOICES = (
        ('legislative', 'Legislative'),
        ('executive', 'Executive'),
        ('judicial', 'Judicial'),
        ('administrative', 'Administrative'),
        ('clerical', 'Clerical'),
    )
    role = models.CharField(max_length=100, choices=ROLE_CHOICES, default='Legislator')
    subdivision = models.ForeignKey(PoliticalSubdivision, on_delete=models.RESTRICT)
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Public Officials"

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def full_name_with_title(self):
        return f'{self.title} {self.first_name} {self.last_name}'

    def __str__(self):
        return self.full_name()


class Committee(CRMBase):
    """
    Represents committees, commissions, or other bodies that review legislation
    before releasing it for final passage.
    """

    name = models.CharField(max_length=255)
    body = models.ForeignKey(GoverningBody, blank=True, on_delete=models.RESTRICT)
    office = models.ForeignKey(PublicOffice, on_delete=models.RESTRICT)

    def __str__(self):
        return self.name


class LegislativeSession(CRMBase):
    """
    Represents legislative sessions, within which bills exist and must be enacted
    before the session ends and the legislative process restarts.
    """

    # TODO: Can this be automated for each defined governing body's
    #  legislative branch?

    body = models.ForeignKey(GoverningBody, on_delete=models.RESTRICT)
    name = models.CharField(blank=True, max_length=255) # TODO: Set based on duration field
    start_date = models.DateField(blank=True)
    end_date = models.DateField(blank=True)


class Legislation(CRMBase):
    """
    Represents proposed or existing legislation related to campaigns.
    """

    name = models.CharField(max_length=255)
    body = models.ForeignKey(GoverningBody, on_delete=models.RESTRICT)
    committee = models.ForeignKey(Committee, blank=True, on_delete=models.RESTRICT)
    session = models.ForeignKey(LegislativeSession, blank=True, on_delete=models.RESTRICT)
    number = models.CharField(blank=True, max_length=255)
    description = models.TextField(blank=True)
    url = models.URLField(blank=True)
    STATUS_CHOICES = (
        ('proposed', 'Proposed'),
        ('in-committee', 'In Committee'),
        ('in-debate', 'In Debate'),
        ('voting-on', 'Voting On'),
        ('adopted', 'Adopted'),
        ('rejected', 'Rejected'),
    )
    status = models.CharField(blank=True, max_length=255, choices=STATUS_CHOICES)

    class Meta:
        verbose_name_plural = 'Legislation'

    def __str__(self):
        return self.name


class SupportLevel(CRMBase):
    """
    lobbying.SupportLevel models the level of support of an individual public
    official for a specific campaign and associated legislation.
    """

    official = models.ForeignKey(PublicOfficial, on_delete=models.PROTECT)
    # I'd prefer to use lower case with underscores for field values, but it's
    # too difficult to reformat in templates
    SUPPORT_LEVEL_CHOICES = (
        ('Strongly Supports', 'Strongly Supports'),
        ('Supports', 'Supports'),
        ('Undecided On', 'Undecided On'),
        ('Opposes', 'Opposes'),
        ('Strongly Opposes', 'Strongly Opposes'),
    )
    campaign = models.ForeignKey(Campaign, on_delete=models.PROTECT)
    campaign_support = models.CharField(max_length=255, choices=SUPPORT_LEVEL_CHOICES)
    # FIXME: What if there are multiple bills involving the campaign?
    # Perhaps have a group/collection of legislation mapped to each campaign?
    legislation = models.ForeignKey(Legislation, null=True, blank=True, on_delete=models.PROTECT)
    legislation_support = models.CharField(max_length=255, choices=SUPPORT_LEVEL_CHOICES)

    class Meta:
        verbose_name_plural = 'Support Levels'

    def __str__(self):
        return f'Support level of {self.official} on {self.campaign}'


class InterpersonalTie(CRMBase):
    """
    lobbying.InterpersonalTie models key relationship data between public
    officials to map out affinity groups and share awareness of influence
    dynamics among the officials via social network analysis. Note that each
    record is only in the context of the first official; the second official
    could have a very different attitude of the relationship.
    """

    # Official one provides the directional perspective for the record
    # Ex. Official 1 has a strongly positive view of Official 2
    official1 = models.ForeignKey('PublicOfficial', related_name='ties_from', on_delete=models.PROTECT)
    official2 = models.ForeignKey('PublicOfficial', related_name='ties_to', on_delete=models.PROTECT)
    TIE_STRENGTH_CHOICES = (
        ('strong', 'Strong'),
        ('weak', 'Weak'),
        ('invisible', 'Invisible'),
        ('unknown', 'Unknown',)
    )
    tie_strength = models.CharField(default='unknown', max_length=10, choices=TIE_STRENGTH_CHOICES)
    TIE_AFFINITY_CHOICES = (
        ('positive', 'Positive'),
        ('neutral', 'Neutral'),
        ('negative', 'Negative'),
    )
    tie_affinity = models.CharField(default='neutral', max_length=10, choices=TIE_AFFINITY_CHOICES)
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Interpersonal Ties'

    def relationship_summary(self):
        return f'{self.official1} is {self.tie_strength}/{self.tie_affinity} towards {self.official2}'

    def __str__(self):
        return f'{self.official1} -> {self.official2}'


