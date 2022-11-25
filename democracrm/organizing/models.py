from django.db import models
from django.db.models import Q

from core.models import CRMBase


class Organization(CRMBase):
    """
    External organizations can be represented this way to track activity at an
    organizational level. If the real-life organization joins the platform, it
    can be associated with the existing object has a proxy for interaction.
    """

    # TODO: Identify how we can track both allies and opponents
    # TODO: Provide org. groups?

    name = models.CharField(max_length=255)
    RELATIONSHIP_CHOICES = (
        ('ally', 'Ally'),
        ('opponent', 'Opponent'),
        ('unknown', 'Unknown'),
    )
    relationship = models.CharField(default='unknown', max_length=255, choices=RELATIONSHIP_CHOICES)
    url = models.URLField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    # Endorsement?
    # Sites, contacts, and social media accounts can be linked to partners

    def __str__(self):
        return self.name


class Platform(CRMBase):
    """
    The platform is the full collection of campaigns that an organization is
    lobbying for, and it used to display, manage, and strategize lobbying efforts.
    """

    # TODO: Should be a singleton instance for the install, created on account
    # initialization

    organization = models.ForeignKey('accounts.Organization', on_delete=models.PROTECT)
    # TODO: Change title to name
    title = models.CharField(null=True, blank=True, max_length=255)
    description = models.TextField()
    categories_enabled = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.organization} Platform'


class PlatformCategory(CRMBase):
    """
    Platform categories can be used to optionally organize campaigns. Must be
    enabled in the platform settings before using.
    """

    platform = models.ForeignKey(Platform, on_delete=models.PROTECT)
    name = models.CharField(null=False, blank=False, max_length=255)
    # TODO: The order field currently is not significant
    order = models.IntegerField(default=1)

    class Meta:
        ordering = ['order']
        verbose_name_plural = "Platform Categories"

    def __str__(self):
        return self.name


class Campaign(CRMBase):
    """
    Campaigns are used to define, organize, and track specific lobbying efforts.
    """

    platform = models.ForeignKey(Platform, on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(PlatformCategory, null=True, blank=True, on_delete=models.PROTECT)
    PRIORITY_CHOICES = (
        (5, 'Top'),
        (4, 'High'),
        (3, 'Medium'),
        (2, 'Low'),
        (1, 'None')
    )
    priority = models.IntegerField(default=3, choices=PRIORITY_CHOICES)
    STATUS_CHOICES = (
        ('brainstorming', 'Brainstorming'),
        ('planned', 'Planned'),
        ('deferred', 'Deferred'),
        ('in-progress', 'In-Progress'),
        ('decision-time', 'Decision Time'),
        ('victory', 'Victory'),
        ('lost', 'Lost'),
    )
    status = models.CharField(default='brainstorming', max_length=255, choices=STATUS_CHOICES)
    targets = models.ManyToManyField('lobbying.PublicOffice')
    # TODO: Add ballot title, legislation view, election date, and other details
    is_public = models.BooleanField(default=False)

    class Meta:
        ordering = ['category', '-priority', 'name']

    # TODO: Add target goals for each public office for legislation passage

    def target_supporters(self):
        return self.supportlevel_set.filter(
            Q(campaign_support='Supports') | Q(campaign_support='Strongly Supports'))

    def target_supporters_count(self):
        return self.target_supporters().count()

    def target_undecided(self):
        return self.supportlevel_set.filter(campaign_support='Undecided On')

    def target_undecided_count(self):
        return self.target_undecided().count()

    def target_opposers(self):
        return self.supportlevel_set.filter(
            Q(campaign_support='Opposes') | Q(campaign_support='Strongly Opposes'))

    def target_opposers_count(self):
        return self.target_opposers().count()

    def target_support_analysis(self):
        analysis = {}
        for target in self.targets.all():
            target_name = target.name
            supporters = self.supportlevel_set.filter()
            analysis[target_name] = []
        return analysis

    def __str__(self):
        return self.name


class Person(CRMBase):
    """
    Provides a record for each person an organization interacts with, linking
    to many other key objects in the CRM.
    """

    user = models.ForeignKey('accounts.User', null=True, blank=True, on_delete=models.PROTECT)
    organization = models.ForeignKey('accounts.Organization', on_delete=models.PROTECT)
    chapter = models.ForeignKey('organizing.Chapter', null=True, blank=True, on_delete=models.PROTECT)
    contact = models.ForeignKey('core.ContactInfo', null=True, blank=True, on_delete=models.PROTECT)
    voter = models.ForeignKey('lobbying.Voter', null=True, blank=True, on_delete=models.PROTECT)
    notes = models.TextField(null=True, blank=True)
    # TODO: board member? other role tracking?

    class Meta:
        verbose_name_plural = 'People'

    def first_name(self):
        return self.user.first_name

    def last_name(self):
        return self.user.last_name

    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'

    def __str__(self):
        return self.user.get_full_name()


class Chapter(CRMBase):
    """
    Regional chapters
    """

    name = models.CharField(max_length=255)
    organization = models.ForeignKey('accounts.Organization',
                                     on_delete=models.PROTECT)
    region = models.ForeignKey('core.Region', on_delete=models.PROTECT)

    def __str__(self):
        return self.name
