import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class Hashtag(models.Model):
    id = models.UUIDField(_('id'), primary_key=True, default=uuid.uuid4)
    created_at = models.DateTimeField(_('date created'), auto_now_add=True)
    updated_at = models.DateTimeField(_('date updated'), auto_now=True)
    name = models.CharField(_('name'), max_length=32)
    user = models.ForeignKey(
        'main.User',
        verbose_name=_('user'),
        on_delete=models.PROTECT
    )

    class Meta:
        ordering = ('-created_at', )
        verbose_name = _('hashtag')
        verbose_name_plural = _('hashtags')


class UserTag(models.Model):
    id = models.UUIDField(_('id'), primary_key=True, default=uuid.uuid4)
    tag = models.ForeignKey(
        'main.Hashtag',
        verbose_name=_('tag'),
        on_delete=models.PROTECT
    )
    user = models.ForeignKey(
        'main.User',
        verbose_name=_('user'),
        on_delete=models.PROTECT
    )

    class Meta:
        verbose_name = _('user tag')
        verbose_name_plural = _('user tags')


class ProjectTag(models.Model):
    id = models.UUIDField(_('id'), primary_key=True, default=uuid.uuid4)
    tag = models.ForeignKey(
        'main.Hashtag',
        verbose_name=_('tag'),
        on_delete=models.PROTECT
    )
    project = models.ForeignKey(
        'main.Project',
        verbose_name=_('project'),
        on_delete=models.PROTECT
    )

    class Meta:
        verbose_name = _('project tag')
        verbose_name_plural = _('project tags')


class IssueTag(models.Model):
    id = models.UUIDField(_('id'), primary_key=True, default=uuid.uuid4)
    tag = models.ForeignKey(
        'main.Hashtag',
        verbose_name=_('tag'),
        on_delete=models.PROTECT
    )
    issue = models.ForeignKey(
        'main.Issue',
        verbose_name=_('issue'),
        on_delete=models.PROTECT
    )

    class Meta:
        verbose_name = _('issue tag')
        verbose_name_plural = _('issue tags')
