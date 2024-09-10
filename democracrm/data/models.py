from pathlib import Path
from django.conf import settings
from django.contrib import admin
from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _

from core.models import CRMBase, CRMTreeBase
from lobbying.models import PublicOffice


class ImportDataSource(CRMBase):

    class DataSourceType(models.TextChoices):
        BULK = 'bulk_upload', _('Bulk Upload')
        API = 'web_api', _('Web API')
        OTHER = 'other', _('Other')

    name = models.CharField()
    source_type = models.CharField(
        default='api',
        choices=DataSourceType.choices
    )
    path = models.FilePathField(
        path=f'{settings.BASE_DIR}/data/imports',
        allow_folders=True,
        allow_files=False,
        recursive=True,
    )
    size = models.IntegerField()

    class Meta:
        verbose_name_plural = 'Import Data Sources'

    def __str__(self):
        return self.name


class ImportDataSet(CRMBase):

    name = models.CharField()

    class Meta:
        verbose_name_plural = 'Import Data Sets'

    def __str__(self):
        return self.name


class WebScraper(CRMBase):

    name = models.CharField()


class PublicOfficeScraper(WebScraper):

    public_office = models.ForeignKey(
        PublicOffice,
        on_delete=models.PROTECT
    )
