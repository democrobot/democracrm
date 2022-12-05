import uuid
from tree_queries.models import TreeNode

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


class CRMTreeBase(CRMBase, TreeNode):
    """
    Base class with efficient hierarchical capabilities.
    """

    class Meta:
        abstract = True
