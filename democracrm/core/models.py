import uuid

from django.db import models  # TODO: Migrate to GeoDjango models
from django.utils.html import format_html


class CRMBase(models.Model):
    """
    Base model for all CRM models.
    """

    uuid = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)
    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    updated_on = models.DateTimeField(auto_now=True, editable=False)
    #TODO: fix object create/update
    #created_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, editable=False)
    #updated_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, editable=False)

    def update(self, update_dict=None, **kwargs):
        """ Helper method to update objects """
        if not update_dict:
            update_dict = kwargs
        update_fields = {'updated_on', 'updated_by'}
        for k, v in update_dict.items():
            setattr(self, k, v)
            update_fields.add(k)
        self.save(update_fields=update_fields)

    class Meta:
        abstract = True


class Comment(CRMBase):
    """
    Comments are text records that can be added to many other objects.
    """
    text = models.TextField()


class Link(CRMBase):
    """
    Links to online resources related to an object.
    """

    name = models.CharField(max_length=255)
    url = models.URLField()
    # Organizations that own links can mark them official
    is_official = models.BooleanField(default=False)


class SocialMediaAccount(CRMBase):
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
