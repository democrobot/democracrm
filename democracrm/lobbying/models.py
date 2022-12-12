from django.contrib import admin
from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _

from core.models import CRMBase, CRMTreeBase
from organizing.models import Campaign


class PoliticalParty(CRMBase):
    """
    A formal political party active with candidates and/or elected officials
    being represented.
    """

    name = models.CharField(
        max_length=255
    )
    description = models.TextField(
        blank=True
    )
    abbreviation = models.CharField(
        blank=True,
        max_length=10
    )
    initial = models.CharField(
        blank=True,
        max_length=1
    )
    notes = models.TextField(
        blank=True
    )
    # TODO: Should parties be linked to boundaries?
    # TODO: Should they be hierarchical since they technically are?

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

    political_party = models.ForeignKey(
        PoliticalParty,
        on_delete=models.RESTRICT
    )
    first_name = models.CharField(
        'First Name',
        blank=True,
        max_length=255
    )
    middle_name = models.CharField(
        'Middle Name',
        blank=True,
        max_length=255
    )
    last_name = models.CharField(
        'Last Name',
        blank=True,
        max_length=255
    )
    sex = models.CharField(
        'Sex',
        blank=True,
        max_length=10
    )
    birth_date = models.DateField(
        'Birth Date',
        blank=True
    )
    initial_registration = models.DateField(
        'Initial Registration',
        blank=True
    )
    current_registration = models.DateField(
        'Current Registration',
        blank=True
    )
    address_number = models.CharField(
        'Address Number',
        blank=True,
        max_length=100
    )
    address_street_direction = models.CharField(
        'Address Street Direction',
        blank=True,
        max_length=100
    )
    address_street_name = models.CharField(
        'Address Street Name',
        blank=True,
        max_length=100
    )
    address_street_type = models.CharField(
        'Address Street Type',
        blank=True,
        max_length=100
    )
    address_unit = models.CharField(
        'Address Unit',
        blank=True,
        max_length=100
    )
    city = models.CharField(
        'City',
        blank=True,
        max_length=100
    )
    state = models.CharField(
        'State',
        blank=True,
        max_length=100
    )
    zip_code = models.CharField(
        'ZIP Code',
        blank=True,
        max_length=100
    )
    phone_number = models.CharField(
        'Phone Number',
        blank=True,
        max_length=11
    )
    email_address = models.CharField(
        'Email',
        blank=True,
        max_length=254
    )

    # TODO: Add point geom field

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

    class Level(models.TextChoices):
        FEDERAL = 'federal', _('Federal')
        STATE = 'state', _('State')
        COUNTY = 'county', _('County')
        MUNICIPAL = 'municipal', _('Municipal')

    name = models.CharField(
        max_length=255
    )
    description = models.TextField(
        blank=True
    )
    level = models.CharField(
        max_length=255,
        choices=Level.choices
    )
    boundary = models.ForeignKey(
        'places.Boundary',
        on_delete=models.RESTRICT
    )
    notes = models.TextField(
        blank=True
    )

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Governing Bodies"

    # TODO: Add point geom field (based on capitol)

    def __str__(self):
        return self.name


class PublicOffice(CRMBase):
    """
    Represents the office that public officials serve within a governing body.
    """

    class Type(models.TextChoices):
        LEGISLATIVE = 'legislative', _('Legislative')
        EXECUTIVE = 'executive', _('Executive')
        JUDICIAL = 'judicial', _('Judicial')
        OTHER = 'other', _('Other')

    type = models.CharField(
        default='legislative',
        max_length=255,
        choices=Type.choices
    )
    governing_body = models.ForeignKey(
        GoverningBody,
        on_delete=models.PROTECT
    )
    name = models.CharField(
        max_length=255
    )
    description = models.TextField(
        blank=True
    )
    total_seats = models.IntegerField(
        default=1
    )
    seats_per_subdivision = models.IntegerField(
        default=1
    )
    notes = models.TextField(
        blank=True
    )

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

    boundary = models.ForeignKey(
        'places.Boundary',
        on_delete=models.RESTRICT
    )
    public_office = models.ForeignKey(
        PublicOffice,
        on_delete=models.PROTECT
    )
    name = models.CharField(
        max_length=255
    )
    description = models.TextField(
        blank=True
    )
    district = models.IntegerField(
        null=True,
        blank=True
    )
    seats = models.IntegerField(
        default=1
    )
    notes = models.TextField(
        blank=True
    )

    # TODO: Add boundary field

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Political Subdivisions'

    def __repr__(self):
        return f'{self.name}'

    def __str__(self):
        return f'{self.name}'

    def governing_body(self):
        return self.public_office.governing_body


class PublicOfficial(CRMBase):
    """
    Represents elected or appointed public officials that are lobbying targets.
    """

    class Role(models.TextChoices):
        LEGISLATIVE = 'legislative', _('Legislative')
        EXECUTIVE = 'executive', _('Executive')
        JUDICIAL = 'judicial', _('Judicial')
        ADMINISTRATIVE = 'administrative', _('Administrative')
        CLERICAL = 'clerical', _('Clerical')

    prefix_name = models.CharField(
        blank=True,
        max_length=50
    )
    first_name = models.CharField(
        max_length=100
    )
    middle_name = models.CharField(
        blank=True,
        max_length=100
    )
    last_name = models.CharField(
        max_length=100
    )
    suffix_name = models.CharField(
        blank=True,
        max_length=50
    )
    role = models.CharField(
        max_length=100,
        choices=Role.choices,
        default=Role.LEGISLATIVE
    )
    public_office = models.ForeignKey(
        PublicOffice,
        blank=True,
        null=True,
        on_delete=models.RESTRICT
    )
    political_subdivision = models.ForeignKey(
        PoliticalSubdivision,
        blank=True,
        null=True,
        on_delete=models.RESTRICT
    )
    title = models.CharField(
        default='Legislator',
        max_length=255
    )
    description = models.TextField(
        blank=True
    )
    is_leadership = models.BooleanField(
        default=False
    )
    leadership_title = models.CharField(
        blank=True,
        max_length=255
    )
    is_elected = models.BooleanField(
        default=True
    )
    is_seeking_reelection = models.BooleanField(
        default=True
    )
    political_party = models.ForeignKey(
        PoliticalParty,
        blank=True,
        null=True,
        on_delete=models.PROTECT
    )
    # TODO: Create term field as range? Might not work for appointed officials.
    service_start = models.DateField(
        null=True,
        blank=True
    )
    service_end = models.DateField(
        null=True,
        blank=True
    )
    official_profile_url = models.URLField(
        blank=True
    )
    official_profile_thumbnail_url = models.URLField(
        blank=True
    )
    official_profile_photo_url = models.URLField(
        blank=True
    )
    notes = models.TextField(
        blank=True
    )

    class Meta:
        ordering = ['last_name']
        verbose_name_plural = 'Public Officials'

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def full_name_with_title(self):
        return f'{self.title} {self.first_name} {self.last_name}'

    def __str__(self):
        return self.full_name()


class PublicOfficialRole(CRMBase):
    """
    Defined governmental roles, attached to public offices (and political subdivisions, where applicable), held by
    specific public officials. These are the positions sought after when people are elected or appointed as public
    officials, and the same public official can hold multiple roles or shift between them in their career.
    """

    class Type(models.TextChoices):
        LEGISLATIVE = 'legislative', _('Legislative')
        EXECUTIVE = 'executive', _('Executive')
        JUDICIAL = 'judicial', _('Judicial')
        ADMINISTRATIVE = 'administrative', _('Administrative')
        CLERICAL = 'clerical', _('Clerical')

    name = models.CharField(
        max_length=255
    )
    description = models.TextField(
        blank=True
    )
    is_elected = models.BooleanField(
        default=True
    )
    is_leadership = models.BooleanField(
        default=False
    )
    leadership_title = models.CharField(
        blank=True,
        max_length=255
    )
    public_office = models.ForeignKey(
        PublicOffice,
        on_delete=models.PROTECT
    )
    political_subdivision = models.ForeignKey(
        PoliticalSubdivision,
        blank=True,
        null=True,
        on_delete=models.PROTECT
    )
    type = models.CharField(
        max_length=100,
        choices=Type.choices,
        default=Type.LEGISLATIVE
    )
    public_official = models.ForeignKey(
        PublicOfficial,
        blank=True,
        null=True,
        on_delete=models.PROTECT
    )
    # TODO: Create term field as range? Might not work for appointed officials.
    service_start = models.DateField(
        null=True,
        blank=True
    )
    service_end = models.DateField(
        null=True,
        blank=True
    )
    official_profile_url = models.URLField(
        blank=True
    )
    official_profile_thumbnail_url = models.URLField(
        blank=True
    )
    official_profile_photo_url = models.URLField(
        blank=True
    )
    notes = models.TextField(
        blank=True
    )

    class Meta:
        verbose_name_plural = 'Public Official Roles'

    def __str__(self):
        return self.name


class PublicOfficialGroup(CRMTreeBase):
    """
    Use to organize public officials.
    """

    name = models.CharField(
        max_length=255
    )
    description = models.TextField(
        blank=True
    )
    public_officials = models.ManyToManyField(
        PublicOfficial,
        blank=True
    )

    class Meta:
        verbose_name_plural = 'Public Official Groups'

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class Committee(CRMTreeBase):
    """
    Represents committees, commissions, or other bodies that review legislation
    before releasing it for final passage.
    """

    # TODO: Enable nest for subcommittees

    name = models.CharField(
        max_length=255
    )
    description = models.TextField(
        blank=True
    )
    governing_body = models.ForeignKey(
        GoverningBody,
        blank=True,
        on_delete=models.RESTRICT
    )
    public_office = models.ForeignKey(
        PublicOffice,
        on_delete=models.RESTRICT
    )
    notes = models.TextField(
        blank=True
    )

    def __str__(self):
        return self.name


class CommitteeRole(CRMBase):
    """
    Roles for each committee.
    """

    class Type(models.TextChoices):
        CHAIR = 'chair', _('Chair')
        VICE_CHAIR = 'vice-chair', _('Vice-Chair')
        EX_OFFICIO = 'officio', _('Ex-Officio')
        MEMBER = 'member', _('Member')

    name = models.CharField(
        max_length=255
    )
    description = models.TextField(
        blank=True
    )
    is_leadership = models.BooleanField(
        default=False
    )
    leadership_title = models.CharField(
        blank=True,
        max_length=255
    )
    type = models.CharField(
        max_length=100,
        choices=Type.choices,
        default=Type.MEMBER
    )
    public_official = models.ForeignKey(
        PublicOfficial,
        blank=True,
        null=True,
        on_delete=models.PROTECT
    )
    # TODO: Create term field as range? Might not work for appointed officials.
    service_start = models.DateField(
        null=True,
        blank=True
    )
    service_end = models.DateField(
        null=True,
        blank=True
    )
    notes = models.TextField(
        blank=True
    )

    class Meta:
        verbose_name_plural = 'Committee Roles'

    def __str__(self):
        return self.name


class LegislativeSession(CRMBase):
    """
    Represents legislative sessions, within which bills exist and must be enacted
    before the session ends and the legislative process restarts.
    """

    # TODO: Can this be automated for each defined governing body's
    # legislative branch?

    governing_body = models.ForeignKey(
        GoverningBody,
        on_delete=models.RESTRICT
    )
    name = models.CharField(
        blank=True,
        max_length=255
    )
    description = models.TextField(
        blank=True
    )
    # TODO: Set based on duration field
    start_date = models.DateField(
        blank=True
    )
    end_date = models.DateField(
        blank=True
    )
    notes = models.TextField(
        blank=True
    )

    class Meta:
        verbose_name_plural = 'Legislative Sessions'

    def __str__(self):
        return self.name


class Legislation(CRMBase):
    """
    Represents proposed or existing legislation related to campaigns.
    """

    class Status(models.TextChoices):
        PROPOSED = 'proposed', _('Proposed')
        IN_COMMITTEE = 'in-committee', _('In Committee')
        IN_DEBATE = 'in-debate', _('In Debate')
        VOTING_ON = 'voting-on', _('Voting On')
        ADOPTED = 'adopted', _('Adopted')
        REJECTED = 'rejected', _('Rejected')

    name = models.CharField(
        max_length=255
    )
    description = models.TextField(
        blank=True
    )
    governing_body = models.ForeignKey(
        GoverningBody,
        on_delete=models.RESTRICT
    )
    committee = models.ForeignKey(
        Committee,
        blank=True,
        on_delete=models.RESTRICT
    )
    legislative_session = models.ForeignKey(
        LegislativeSession,
        blank=True,
        on_delete=models.RESTRICT
    )
    number = models.CharField(
        blank=True,
        max_length=255
    )
    url = models.URLField(
        blank=True
    )
    status = models.CharField(
        blank=True,
        max_length=255,
        choices=Status.choices
    )
    notes = models.TextField(
        blank=True
    )

    class Meta:
        verbose_name_plural = 'Legislation'

    def __str__(self):
        return self.name


class LegislationGroup(CRMBase):
    """
    Used to group legislation for campaign tracking (i.e. House and Senate bills for same campaign, etc.)
    """

    name = models.CharField(
        max_length=255
    )
    description = models.TextField(
        blank=True
    )
    legislation = models.ManyToManyField(
        Legislation,
        blank=True
    )
    notes = models.TextField(
        blank=True
    )


class SupportLevel(CRMBase):
    """
    lobbying.SupportLevel models the level of support of an individual public
    official for a specific campaign and associated legislation.
    """

    # FIXME: I'd prefer to use lower case with underscores for field values, but it's
    # too difficult to reformat in templates
    class Status(models.TextChoices):
        STRONGLY_SUPPORTS = 'Strongly Supports', _('Strongly Supports')
        SUPPORTS = 'Supports', _('Supports')
        UNDECIDED_ON = 'Undecided On', _('Undecided On')
        OPPOSES = 'Opposes', _('Opposes')
        STRONGLY_OPPOSES = 'Strongly Opposes', _('Strongly Opposes')

    public_official = models.ForeignKey(
        PublicOfficial,
        on_delete=models.PROTECT
    )
    campaign = models.ForeignKey(
        Campaign,
        on_delete=models.PROTECT
    )
    campaign_support = models.CharField(
        max_length=255,
        choices=Status.choices
    )
    legislation = models.ForeignKey(
        LegislationGroup,
        null=True,
        blank=True,
        on_delete=models.PROTECT
    )
    legislation_support = models.CharField(
        max_length=255,
        choices=Status.choices
    )
    notes = models.TextField(
        blank=True
    )

    class Meta:
        verbose_name_plural = 'Support Levels'

    def __str__(self):
        return f'Support level of {self.public_official} on {self.campaign}'


class InterpersonalTie(CRMBase):
    """
    lobbying.InterpersonalTie models key relationship data between public
    officials to map out affinity groups and share awareness of influence
    dynamics among the officials via social network analysis. Note that each
    record is only in the context of the first official; the second official
    could have a very different attitude of the relationship.
    """

    class TieStrength(models.TextChoices):
        STRONG = 'strong', _('Strong')
        WEAK = 'weak', _('Weak')
        INVISIBLE = 'invisible', _('Invisible')
        UNKNOWN = 'unknown', _('Unknown')

    class TieAffinity(models.TextChoices):
        POSITIVE = 'positive', _('Positive')
        NEUTRAL = 'neutral', _('Neutral')
        NEGATIVE = 'negative', _('Negative')

    # Official one provides the directional perspective for the record
    # Ex. Official 1 has a strongly positive view of Official 2
    public_official1 = models.ForeignKey(
        'PublicOfficial',
        related_name='ties_from',
        on_delete=models.PROTECT
    )
    public_official2 = models.ForeignKey(
        'PublicOfficial',
        related_name='ties_to',
        on_delete=models.PROTECT
    )
    tie_strength = models.CharField(
        default='unknown',
        max_length=10,
        choices=TieStrength.choices
    )
    tie_affinity = models.CharField(
        default='neutral',
        max_length=10,
        choices=TieAffinity.choices
    )
    notes = models.TextField(
        blank=True
    )

    class Meta:
        verbose_name_plural = 'Interpersonal Ties'

    def relationship_summary(self):
        return f'{self.public_official1} is {self.tie_strength}/{self.tie_affinity} towards {self.public_official2}'

    def __str__(self):
        return f'{self.public_official1} -> {self.public_official2}'
