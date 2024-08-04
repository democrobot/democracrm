from django.contrib import admin
from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _

from core.models import CRMBase, CRMTreeBase
from lobbying.models import PublicOffice

class WebScraper(CRMBase):

    name = models.CharField()


class PublicOfficeScraper(WebScraper):

    public_office = models.ForeignKey(
        PublicOffice,
        on_delete=models.PROTECT
    )
