import uuid
from django.db import models
from django.utils.html import format_html


class SocialMediaAccount(models.Model):
    """
    A social media account that should be tracked and/or engaged with.
    """
    PLATFORMS = (
        ('twitter', 'Twitter'),
        ('instagram', 'Instagram'),
        ('facebook', 'Facebook'),
        ('linkedin', 'LinkedIn'),
    )
    platform = models.CharField(null=False, max_length=255, choices=PLATFORMS)
    handle = models.CharField(null=False, blank=False, max_length=255)
    voter = models.ForeignKey('Voter', null=True, blank=True, on_delete=models.RESTRICT)

    class Meta:
        verbose_name_plural = "Social Media Accounts"

    def __repr__(self):
        return self.handle

    def __str__(self):
        return f'@{self.handle}'

    def url(self):
        if self.platform == 'twitter':
            url_text = f'https://www.twitter.com/{self.handle}'
            return format_html('<a href="{url}">{url}</a>', url=url_text)
        elif self.platform == 'instagram':
            url_text = f'https://www.instagram.com/{self.handle}'
            return format_html('<a href="{url}">{url}</a>', url=url_text)
        elif self.platform == 'facebook':
            url_text = f'https://www.facebook.com/{self.handle}'
            return format_html('<a href="{url}">{url}</a>', url=url_text)
        elif self.platform == 'linkedin':
            url_text = f'https://www.linkedin.com/in/{self.handle}'
            return format_html('<a href="{url}">{url}</a>', url=url_text)
        else:
            return 'N/A'


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

    #uuid = models.UUIDField('UUID', default=uuid.uuid4)
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



