import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class TimelineItem(models.Model):
    id = models.UUIDField(_('id'), primary_key=True, default=uuid.uuid4)
    created_at = models.DateTimeField(_('date created'), auto_now_add=True)
    updated_at = models.DateTimeField(_('date updated'), auto_now=True)
    is_archived = models.BooleanField(_('archive'), default=False)
    is_read = models.BooleanField(_('read'), default=False)
    is_actioned = models.BooleanField(_('action'), default=False)
    message = models.TextField(_('message'), blank=True)
    user = models.ForeignKey(
        'main.User',
        verbose_name=_('user'),
        on_delete=models.PROTECT
    )
    issue = models.ForeignKey(
        'main.Issue',
        verbose_name=_('issue'),
        on_delete=models.PROTECT
    )

    class Meta:
        ordering = ('-created_at', )
        verbose_name = _('timeline item')
        verbose_name_plural = _('timeline items')
