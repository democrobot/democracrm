from django.contrib.gis.db import models
from django.contrib.gis.db.models import Q
from django.utils.translation import gettext_lazy as _

from accounts.models import UserAccount, OrganizationAccount
from contacts.models import Contact
from core.models import CRMBase, CRMTreeBase, OrgAccountMixin
# from lobbying.models import Voter, PublicOffice  # FIXME: Circular reference issue
from places.models import Region, Site


class OrganizationGroup(CRMTreeBase, OrgAccountMixin):
    """
    Provides hierarchical groupings of similar organizations.
    """

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Organization Groups'

    def __str__(self):
        return self.name


class Organization(CRMBase, OrgAccountMixin):
    """
    External organizations can be represented this way to track activity at an
    organizational level. If the real-life organization joins the platform, it
    can be associated with the existing object as a proxy for interaction.
    """

    # TODO: Identify how we can track both allies and opponents
    # TODO: Provide org. groups?
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    group = models.ForeignKey(OrganizationGroup, null=True, blank=True, on_delete=models.RESTRICT)
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
    site = models.ForeignKey(Site, null=True, blank=True, on_delete=models.PROTECT)
    # contacts

    # TODO: Should organizations have boundaries or regions?
    # TODO: Can they be used to manage endorsement?
    # Sites, contacts, and social media accounts can be linked to organizations, as well

    def __str__(self):
        return self.name


class CampaignCategory(CRMBase, OrgAccountMixin):
    """
    Campaign categories can be used to optionally organize campaigns.
    """

    name = models.CharField(max_length=255)
    # TODO: The order field currently is not significant
    order = models.IntegerField(default=1)

    class Meta:
        ordering = ['order']
        verbose_name_plural = "Campaign Categories"

    def __str__(self):
        return self.name


class Campaign(CRMBase, OrgAccountMixin):
    """
    Campaigns are used to define, organize, and track specific lobbying efforts.
    """

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.ForeignKey(CampaignCategory, null=True, blank=True, on_delete=models.PROTECT)
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
    # TODO: Break out targets as progress milestones, and include other steps in the process (draft bill, committee
    # approval, etc.

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


class CampaignMilestone(CRMBase, OrgAccountMixin):
    """

    """

    campaign = models.ForeignKey(Campaign, on_delete=models.PROTECT)
    status = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Campaign Milestones'
    
    def __str__(self):
        return self.status


class Chapter(CRMBase, OrgAccountMixin):
    """
    Regional chapters
    """

    name = models.CharField(max_length=255)
    region = models.ForeignKey(Region, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class PersonGroup(CRMTreeBase, OrgAccountMixin):
    """
    Provides hierarchical groups that people can be included within.
    """

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Person Group'
    
    def __str__(self):
        return self.name


class Person(CRMBase, OrgAccountMixin):
    """
    Provides a record for each person participating in the organization, centrally linking
    to many other key objects in the CRM.
    """

    user_account = models.ForeignKey(UserAccount, null=True, blank=True, on_delete=models.PROTECT)
    chapter = models.ForeignKey(Chapter, null=True, blank=True, on_delete=models.PROTECT)
    contact = models.ForeignKey(Contact, null=True, blank=True, on_delete=models.PROTECT)
    voter = models.ForeignKey('lobbying.Voter', null=True, blank=True, on_delete=models.PROTECT)
    groups = models.ManyToManyField(PersonGroup)
    notes = models.TextField(blank=True)
    # TODO: board member? other role tracking?

    class Meta:
        verbose_name_plural = 'People'

    def __str__(self):
        if self.user_account:
            return self.user_account.get_full_name()
        else:
            return 'Unknown - Link a Record!'

    def first_name(self):
        return self.user_account.first_name

    def last_name(self):
        return self.user_account.last_name

    def full_name(self):
        return f'{self.user_account.first_name} {self.user_account.last_name}'


class Relationship(CRMBase):
    """
    Track relationships between people and organizations.
    """

    class RelationshipClass(models.TextChoices):
        PERSON_TO_PERSON = 'person_to_person', _('Person to Person')
        PERSON_TO_ORG = 'person_to_org', _('Person to Organization')
        ORG_TO_ORG = 'org_to_org', _('Organization to Organization')
    
    #class RelationshipType(models.TextChoices):
    [
        # Person to person:
        'Assistant to',
        'Assisted by',
        'Child of',
        'Friend of',
        'Manager of',
        'Mentee of',
        'Mentor of',
        'Parent of',
        'Partner of',
        'Reports to',
        'Sibling of',
        'Spouse of',
        'Student of',
        'Teacher of',
        # Person to organization:
        'Alum of',
        'Board member of',
        'Consultant to',
        'Employee of',
        'Member of',
        'Primary contact of',
        'Resident of',
        'Student at',
        'Candidate of',
        'Treasurer of',
        # Organization to person
        'Alum',
        'Board member',
        'Employer of',
        'Member',
        'Primary contact',
        'Resident',
        'School of',
        'Candidate',
        'Treasurer',
        # Organization to organization
        'Affiliate',
        'Chapter',
        'Chapter of',
        'Organization partner',
        'Parent company of',
        'Subsidiary of',
    ]