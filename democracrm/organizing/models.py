from django.contrib.gis.db import models
from django.contrib.gis.db.models import Q

from accounts.models import UserAccount, OrganizationAccount
from contacts.models import Contact
from core.models import CRMBase
# from lobbying.models import Voter, PublicOffice  # FIXME: Circular reference issue
from places.models import Region


class Organization(CRMBase):
    """
    External organizations can be represented this way to track activity at an
    organizational level. If the real-life organization joins the platform, it
    can be associated with the existing object has a proxy for interaction.
    """

    # TODO: Identify how we can track both allies and opponents
    # TODO: Provide org. groups?

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    # FIXME: Update to Django choices model
    RELATIONSHIP_CHOICES = (
        ('ally', 'Ally'),
        ('opponent', 'Opponent'),
        ('unknown', 'Unknown'),
    )
    relationship = models.CharField(default='unknown', max_length=255, choices=RELATIONSHIP_CHOICES)
    url = models.URLField(blank=True)
    notes = models.TextField(blank=True)
    region = models.ForeignKey(Region, null=True, blank=True, on_delete=models.PROTECT)
    # TODO: Should organizations have boundaries or regions?
    # TODO: Can they be used to manage endorsement?
    # Sites, contacts, and social media accounts can be linked to organizations, as well

    def __str__(self):
        return self.name


class Platform(CRMBase):
    """
    The platform is the full collection of campaigns that an organization is
    lobbying for, and it used to display, manage, and strategize lobbying efforts.
    """

    # TODO: Should be a singleton instance for the install, created on account
    # initialization

    org_account = models.ForeignKey(OrganizationAccount, on_delete=models.PROTECT)
    # TODO: Change title to name
    title = models.CharField(blank=True, max_length=255)
    description = models.TextField(blank=True)
    categories_enabled = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.org_account} Platform'


class PlatformCategory(CRMBase):
    """
    Platform categories can be used to optionally organize campaigns. Must be
    enabled in the platform settings before using.
    """

    platform = models.ForeignKey(Platform, on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
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
    description = models.TextField(blank=True)
    category = models.ForeignKey(PlatformCategory, null=True, blank=True, on_delete=models.PROTECT)
    start_date = models.DateField(
        null=True,
        blank=True
    )
    end_date = models.DateField(
        null=True,
        blank=True
    )
    # FIXME: Update to Django choices model
    PRIORITY_CHOICES = (
        (5, 'Top'),
        (4, 'High'),
        (3, 'Medium'),
        (2, 'Low'),
        (1, 'None')
    )
    priority = models.IntegerField(default=3, choices=PRIORITY_CHOICES)
    # FIXME: Update to Django choices model
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
    targets = models.ManyToManyField('lobbying.PublicOffice', blank=True)
    # TODO: Add ballot title, legislation view, election date, and other details
    legislation = models.ForeignKey(
        'lobbying.LegislationGroup',
        null=True,
        blank=True,
        on_delete=models.PROTECT
    )
    is_public = models.BooleanField(default=False)

    class Meta:
        ordering = ['category', '-priority', 'name']

    def __str__(self):
        return self.name

    def priority_label(self):
        labels = {
            5: 'top',
            4: 'high',
            3: 'medium',
            2: 'low',
            1: 'none'
        }
        return labels[self.priority]

    def status_card(self):
        if self.status == 'in-progress':
            return 'text-bg-success'
        else:
            return 'text-bg-light'

    # TODO: Add target goals for each public office for legislation passage

    # TODO: Should these methods be in the SupportLevel model?

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


class Chapter(CRMBase):
    """
    Regional chapters
    """

    name = models.CharField(max_length=255)
    org_account = models.ForeignKey(OrganizationAccount, on_delete=models.PROTECT)
    region = models.ForeignKey(Region, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Person(CRMBase):
    """
    Provides a record for each person an organization interacts with, linking
    to many other key objects in the CRM.
    """

    user_account = models.ForeignKey(UserAccount, blank=True, on_delete=models.PROTECT)
    org_account = models.ForeignKey(OrganizationAccount, on_delete=models.PROTECT)
    chapter = models.ForeignKey(Chapter, null=True, blank=True, on_delete=models.PROTECT)
    contact = models.ForeignKey(Contact, null=True, blank=True, on_delete=models.PROTECT)
    voter = models.ForeignKey('lobbying.Voter', null=True, blank=True, on_delete=models.PROTECT)
    notes = models.TextField(blank=True)
    # TODO: board member? other role tracking?

    class Meta:
        verbose_name_plural = 'People'

    def __str__(self):
        return self.user_account.get_full_name()

    def first_name(self):
        return self.user_account.first_name

    def last_name(self):
        return self.user_account.last_name

    def full_name(self):
        return f'{self.user_account.first_name} {self.user_account.last_name}'





