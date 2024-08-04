import requests
from django.contrib.gis.db import models

from core.models import CRMBase


class Link(CRMBase):
    """
    Links to online resources related to an object.
    """

    name = models.CharField(max_length=255)
    url = models.URLField(blank=True)
    # Organizations that own links can mark them official
    is_official = models.BooleanField(default=False)

    def url_responding(self):
        response = requests.get(self.url)
        try:
            if response.status_code == 200:
                return True
            else:
                return False
        except ConnectionError:
            return False


class SocialMediaAccount(CRMBase):
    """
    A social media account that should be tracked and/or engaged with.
    """

    PLATFORMS = (
        ('twitter', 'Twitter'), ## TODO: Update to X
        ('instagram', 'Instagram'),
        ('facebook', 'Facebook'),
        ('linkedin', 'LinkedIn'),
    )
    platform = models.CharField(max_length=255, choices=PLATFORMS)
    handle = models.CharField(blank=False, max_length=255)

    class Meta:
        verbose_name_plural = "Social Media Accounts"

    def __repr__(self):
        return self.handle

    def __str__(self):
        # Doesn't always use the @-style handle
        return f'@{self.handle}'

    def url(self):
        # FIXME
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
