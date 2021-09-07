import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class Notification(models.Model):
    id = models.UUIDField(_('id'), primary_key=True, default=uuid.uuid4)
    created_at = models.DateTimeField(_('date created'), auto_now_add=True)
    is_read = models.BooleanField(_('read'), default=False)
    is_archived = models.BooleanField(_('archive'), default=False)
    path = models.CharField(_('path'), max_length=128, blank=True)
    url = models.URLField(_('url'), blank=True)
    message = models.CharField(_('message'), max_length=1024)
    avatar_url = models.URLField(_('avatar_url'), blank=True)
    user = models.ForeignKey(
        'main.User',
        verbose_name=_('user'),
        on_delete=models.PROTECT
    )

    class Meta:
        ordering = ('-created_at', )
        verbose_name = _('notification')
        verbose_name_plural = _('notifications')
