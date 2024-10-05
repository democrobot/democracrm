from django.contrib import admin
from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _

from core.models import CRMBase, CRMTreeBase
from organizing.models import Campaign
from places.models import Boundary


class PoliticalParty(CRMBase):
    """
    A formal political party active with candidates and/or elected officials
    being represented.
    """

    name = models.CharField()
    description = models.TextField(blank=True)
    abbreviation = models.CharField(blank=True)
    initial = models.CharField(blank=True)
    notes = models.TextField(blank=True)
    # TODO: Should parties be linked to boundaries?
    # TODO: Should they be hierarchical since they technically are?

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Political Parties'


class Voter(CRMBase):
    """
    An individual voter record.
    """

    class Status(models.TextChoices):
        ACTIVE = 'active', _('Active')
        INACTIVE = 'inactive', _('Inactive')

    id = models.CharField(primary_key=True)
    political_party = models.ForeignKey(
        PoliticalParty,
        on_delete=models.RESTRICT,
    )
    # Store original party code to ensure all party mappings can be made
    political_party_code = models.CharField()
    prefix_name = models.CharField(
        'Prefix Name',
        blank=True,
    )
    first_name = models.CharField(
        'First Name',
        blank=True,
    )
    middle_name = models.CharField(
        'Middle Name',
        blank=True,
    )
    last_name = models.CharField(
        'Last Name',
        blank=True,
    )
    suffix_name = models.CharField(
        'Suffix Name',
        blank=True,
    )
    sex = models.CharField(
        'Sex',
        blank=True,
    )
    birth_date = models.DateField(
        'Birth Date',
        null=True,
        blank=True,
    )
    initial_registration_date = models.DateField(
        'Initial Registration',
        null=True,
        blank=True,
    )
    last_registration_date = models.DateField(
        'Current Registration',
        null=True,
        blank=True,
    )
    last_election_date = models.DateField(
        null=True,
        blank=True,
    )
    last_voting_date = models.DateField(
        null=True,
        blank=True,
    )
    voter_precinct = models.CharField(blank=True)
    voter_polling_place = models.CharField(blank=True)
    status = models.CharField(
        choices=Status.choices,
        default=Status.ACTIVE,
    )
    physical_address_street_number = models.CharField(
        'Address Number',
        blank=True,
    )
    physical_address_street_number_suffix = models.CharField(blank=True)
    physical_address_street_name = models.CharField(
        'Address Street Name',
        blank=True,
    )
    physical_address_unit = models.CharField(
        'Address Unit',
        blank=True,
    )
    physical_address_supplemental = models.CharField(
        'Address Supplement',
        blank=True,
    )
    physical_address_city = models.CharField(
        'City',
        blank=True,
    )
    municipality = models.ForeignKey(
        Boundary,
        blank=True,
        null=True,
        related_name='municipal_voters',
        on_delete=models.SET_NULL,
    )
    # Store original municipality code to ensure all municipality mappings can be made
    municipality_code = models.CharField()
    county = models.ForeignKey(
        Boundary,
        blank=True,
        null=True,
        related_name='county_voters',
        on_delete=models.SET_NULL,
    )
    state = models.ForeignKey(
        Boundary,
        blank=True,
        null=True,
        related_name='state_voters',
        on_delete=models.SET_NULL,
    )
    physical_address_zip_code = models.CharField(
        'ZIP Code',
        blank=True,
    )
    mailing_address = models.CharField(
        'Mailing Address',
        blank=True,
    )
    mailing_address_supplemental = models.CharField(
        'Mailing Address Supplement',
        blank=True,
    )
    mailing_address_city = models.CharField(
        'Mailing City',
        blank=True,
    )
    mailing_address_state = models.CharField(
        'Mailing State',
        blank=True,
    )
    mailing_address_zip_code = models.CharField(
        'Mailing ZIP Code',
        blank=True,
    )
    phone_number = models.CharField(
        'Phone Number',
        blank=True,
    )
    email_address = models.CharField(
        'Email',
        blank=True,
    )
    data_export_date = models.DateField()

    # TODO: Add point geom field

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def full_name(self):
        if self.first_name and self.last_name:
            return str(self)
        else:
            return 'N/A'

    def short_physical_address(self):
        street_number = self.physical_address_street_number
        street_number_suffix = self.physical_address_street_number_suffix
        street_number_supplemental = self.physical_address_supplemental
        print(street_number_supplemental)
        street_name = self.physical_address_street_name
        unit = self.physical_address_unit
        print(unit)

        if unit and not street_number_supplemental:
            address = f'{street_number}{street_number_suffix} {street_name} Unit {unit}'
        elif street_number_supplemental and not unit:
            address = f'{street_number}{street_number_suffix} {street_name} {street_number_supplemental}'
        elif unit and street_number_supplemental:
            address = f'{street_number}{street_number_suffix} {street_name} {street_number_supplemental} Unit {unit}'
        else:
            address = f'{street_number}{street_number_suffix} {street_name}'

        return address

    def full_physical_address(self):
        street_number = self.physical_address_street_number
        street_number_suffix = self.physical_address_street_number_suffix
        street_name = self.physical_address_street_name
        city = self.physical_address_city
        state = self.state
        zip_code = self.physical_address_zip_code

        # TODO: Add unit and supplementals
        address = f'{street_number}{street_number_suffix} {street_name} {city} {str(state).upper()} {zip_code}'

        return address


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

    name = models.CharField()
    description = models.TextField(blank=True)
    level = models.CharField(choices=Level.choices)
    boundary = models.ForeignKey(
        'places.Boundary',
        on_delete=models.RESTRICT,
    )
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Governing Bodies'

    # TODO: Add point geom field (based on capitol)

    def __str__(self):
        return self.name


class PublicOffice(CRMTreeBase):
    """
    Represents the office that public officials serve within a governing body.
    """

    class OfficeType(models.TextChoices):
        LEGISLATIVE = 'legislative', _('Legislative')
        EXECUTIVE = 'executive', _('Executive')
        JUDICIAL = 'judicial', _('Judicial')
        OTHER = 'other', _('Other')

    class ChamberType(models.TextChoices):
        UNICAMERAL = 'unicameral', _('Unicameral')
        BICAMERAL = 'bicameral', _('Bicameral')
        TRICAMERAL = 'tricameral', _('Tricameral')
        TETRACAMERAL = 'tetracameral', _('Tetracameral')

    governing_body = models.ForeignKey(
        GoverningBody,
        on_delete=models.PROTECT,
    )

    office_type = models.CharField(
        default='legislative',
        choices=OfficeType.choices,
    )

    # TODO: Only display when office_type is legislative
    chamber_type = models.CharField(
        default='unicameral',
        choices=ChamberType.choices,
    )

    # TODO: Define chamber order (i.e. Upper House, Lower House) via sort index?

    name = models.CharField()
    description = models.TextField(blank=True)
    total_seats = models.IntegerField(
        # TODO: Can this be the total of child objects?
        default=1,
    )
    seats_per_subdivision = models.IntegerField(default=1)
    notes = models.TextField(blank=True)

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
        on_delete=models.RESTRICT,
    )
    public_office = models.ForeignKey(
        PublicOffice,
        on_delete=models.PROTECT,
    )
    name = models.CharField()
    description = models.TextField(blank=True)
    district = models.IntegerField(
        null=True,
        blank=True,
    )
    seats = models.IntegerField(default=1)
    notes = models.TextField(blank=True)

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

    prefix_name = models.CharField(blank=True)
    first_name = models.CharField()
    middle_name = models.CharField(blank=True)
    last_name = models.CharField()
    suffix_name = models.CharField(blank=True)
    role = models.CharField(
        choices=Role.choices,
        default=Role.LEGISLATIVE,
    )
    public_office = models.ForeignKey(
        PublicOffice,
        blank=True,
        null=True,
        on_delete=models.RESTRICT,
    )
    political_subdivision = models.ForeignKey(
        PoliticalSubdivision,
        blank=True,
        null=True,
        on_delete=models.RESTRICT,
    )
    title = models.CharField(default='Legislator')
    description = models.TextField(blank=True)
    is_leadership = models.BooleanField(default=False)
    leadership_title = models.CharField(blank=True)
    is_elected = models.BooleanField(default=True)
    is_seeking_reelection = models.BooleanField(default=True)
    political_party = models.ForeignKey(
        PoliticalParty,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
    )
    # TODO: Create term field as range? Might not work for appointed officials.
    service_start = models.DateField(
        null=True,
        blank=True,
    )
    service_end = models.DateField(
        null=True,
        blank=True,
    )
    official_profile_url = models.URLField(blank=True)
    official_profile_thumbnail_url = models.URLField(blank=True)
    official_profile_photo_url = models.URLField(blank=True)
    contacts = models.ManyToManyField(
        'contacts.Contact',
        blank=True,
    )
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['last_name']
        verbose_name_plural = 'Public Officials'

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def full_name_with_title(self):
        return f'{self.title} {self.first_name} {self.last_name}'

    def __str__(self):
        return self.full_name()


class PublicOfficialPosition(CRMBase):
    """
    Defined governmental positions, attached to public offices (and political subdivisions, where applicable), held by
    specific public officials. These are the positions sought after when people are elected or appointed as public
    officials, and the same public official can hold multiple position or shift between them in their career.
    """

    class Type(models.TextChoices):
        LEGISLATIVE = 'legislative', _('Legislative')
        EXECUTIVE = 'executive', _('Executive')
        JUDICIAL = 'judicial', _('Judicial')
        ADMINISTRATIVE = 'administrative', _('Administrative')
        CLERICAL = 'clerical', _('Clerical')

    name = models.CharField()
    description = models.TextField(blank=True)
    is_elected = models.BooleanField(default=True)
    is_leadership = models.BooleanField(default=False)
    leadership_title = models.CharField(blank=True)
    public_office = models.ForeignKey(
        PublicOffice,
        on_delete=models.PROTECT,
    )
    political_subdivision = models.ForeignKey(
        PoliticalSubdivision,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
    )
    type = models.CharField(
        choices=Type.choices,
        default=Type.LEGISLATIVE,
    )
    public_official = models.ForeignKey(
        PublicOfficial,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
    )
    # TODO: Create term field as range? Might not work for appointed officials.
    start_date = models.DateField(
        null=True,
        blank=True,
    )
    end_date = models.DateField(
        null=True,
        blank=True,
    )
    official_profile_url = models.URLField(blank=True)
    official_profile_thumbnail_url = models.URLField(blank=True)
    official_profile_photo_url = models.URLField(blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Public Official Positions'

    def __str__(self):
        return self.name


class PublicOfficialGroup(CRMTreeBase):
    """
    Used to organize public officials.
    """

    name = models.CharField()
    description = models.TextField(blank=True)
    public_officials = models.ManyToManyField(
        PublicOfficial,
        blank=True,
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

    name = models.CharField()
    description = models.TextField(blank=True)
    governing_body = models.ForeignKey(
        GoverningBody,
        blank=True,
        on_delete=models.RESTRICT,
    )
    public_office = models.ForeignKey(
        PublicOffice,
        on_delete=models.RESTRICT,
    )
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.name


class CommitteeRole(CRMBase):
    """
    Roles for each committee.
    """

    class Type(models.TextChoices):
        CHAIR = 'chair', _('Chair')
        VICE_CHAIR = 'vice-chair', _('Vice-Chair')
        EX_OFFICIO = 'ex-officio', _('Ex-Officio')
        MEMBER = 'member', _('Member')

    name = models.CharField()
    description = models.TextField(blank=True)
    is_leadership = models.BooleanField(default=False)
    leadership_title = models.CharField(blank=True)
    type = models.CharField(
        choices=Type.choices,
        default=Type.MEMBER,
    )
    public_official = models.ForeignKey(
        PublicOfficial,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
    )
    # TODO: Create term field as range? Might not work for appointed officials.
    service_start = models.DateField(
        null=True,
        blank=True,
    )
    service_end = models.DateField(
        null=True,
        blank=True,
    )
    notes = models.TextField(blank=True)

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
        on_delete=models.RESTRICT,
    )
    name = models.CharField(blank=True)
    description = models.TextField(blank=True)
    # TODO: Set based on duration field
    start_date = models.DateField(blank=True)
    end_date = models.DateField(blank=True)
    notes = models.TextField(blank=True)

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

    # Status fields for US Congress
    # Introduced
    # Committee Consideration
    # Floor Consideration
    # Failed One Chamber
    # Passed One Chamber
    # Passed Both Chambers
    # Resolving Differences
    # To President
    # Veto Actions
    # Became Law

    name = models.CharField()
    description = models.TextField(blank=True)
    governing_body = models.ForeignKey(
        GoverningBody,
        on_delete=models.RESTRICT,
    )
    committee = models.ForeignKey(
        Committee,
        blank=True,
        on_delete=models.RESTRICT,
    )
    legislative_session = models.ForeignKey(
        LegislativeSession,
        blank=True,
        on_delete=models.RESTRICT,
    )
    number = models.CharField(blank=True)
    url = models.URLField(blank=True)
    status = models.CharField(
        blank=True,
        choices=Status.choices,
    )
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Legislation'

    def __str__(self):
        return self.name


class LegislationGroup(CRMBase):
    """
    Used to group legislation for campaign tracking (i.e. House and Senate bills for same campaign, etc.)
    """

    name = models.CharField()
    description = models.TextField(blank=True)
    legislation = models.ManyToManyField(
        Legislation,
        blank=True,
    )
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Legislation Group'

    def __str__(self):
        return self.name


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
        on_delete=models.PROTECT,
    )
    campaign = models.ForeignKey(
        Campaign,
        on_delete=models.PROTECT,
    )
    campaign_support = models.CharField(choices=Status.choices)
    legislation = models.ForeignKey(
        LegislationGroup,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    legislation_support = models.CharField(choices=Status.choices)
    notes = models.TextField(blank=True)

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
        on_delete=models.PROTECT,
    )
    public_official2 = models.ForeignKey(
        'PublicOfficial',
        related_name='ties_to',
        on_delete=models.PROTECT,
    )
    tie_strength = models.CharField(
        default='unknown',
        choices=TieStrength.choices,
    )
    tie_affinity = models.CharField(
        default='neutral',
        choices=TieAffinity.choices,
    )
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Interpersonal Ties'

    def relationship_summary(self):
        return f'{self.public_official1} is {self.tie_strength}/{self.tie_affinity} towards {self.public_official2}'

    def __str__(self):
        return f'{self.public_official1} -> {self.public_official2}'
