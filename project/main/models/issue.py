import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class Issue(models.Model):
    id = models.UUIDField(_('id'), primary_key=True, default=uuid.uuid4)
    created_at = models.DateTimeField(_('date created'), auto_now_add=True)
    updated_at = models.DateTimeField(_('date updated'), auto_now=True)
    is_archived = models.BooleanField(_('archive'), default=False)
    is_open = models.BooleanField(_('public'), default=True)
    title = models.CharField(_('title'), max_length=64, blank=True)
    content = models.TextField(_('content'), blank=True)
    user = models.ForeignKey(
        'main.User',
        verbose_name=_('user'),
        on_delete=models.PROTECT
    )
    project = models.ForeignKey(
        'main.Project',
        verbose_name=_('project'),
        on_delete=models.PROTECT
    )
    mention = models.ForeignKey(
        'self',
        verbose_name=_('mention'),
        on_delete=models.PROTECT,
        null=True
    )

    class Meta:
        ordering = ('-created_at', )
        verbose_name = _('issue')
        verbose_name_plural = _('issues')


class IssueAttachment(models.Model):
    id = models.UUIDField(_('id'), primary_key=True, default=uuid.uuid4)
    created_at = models.DateTimeField(_('date created'), auto_now_add=True)
    is_archived = models.BooleanField(_('archive'), default=False)
    title = models.CharField(_('title'), max_length=64)
    url = models.URLField(_('url'))
    issue = models.ForeignKey(
        'main.Issue',
        verbose_name=_('issue'),
        on_delete=models.PROTECT
    )
    user = models.ForeignKey(
        'main.User',
        verbose_name=_('user'),
        on_delete=models.PROTECT
    )

    class Meta:
        ordering = ('-created_at', )
        verbose_name = _('issue attachment')
        verbose_name_plural = _('issue attachments')


class IssueMention(models.Model):
    id = models.UUIDField(_('id'), primary_key=True, default=uuid.uuid4)
    issue = models.ForeignKey(
        'main.Issue',
        verbose_name=_('issue'),
        on_delete=models.PROTECT
    )
    user = models.ForeignKey(
        'main.User',
        verbose_name=_('user'),
        on_delete=models.PROTECT
    )

    class Meta:
        verbose_name = _('issue mention')
        verbose_name_plural = _('issue mentions')


class IssueReaction(models.Model):
    id = models.UUIDField(_('id'), primary_key=True, default=uuid.uuid4)
    issue = models.ForeignKey(
        'main.Issue',
        verbose_name=_('issue'),
        on_delete=models.PROTECT
    )
    user = models.ForeignKey(
        'main.User',
        verbose_name=_('user'),
        on_delete=models.PROTECT
    )
    reaction = models.CharField(_('reaction'), max_length=1)

    class Meta:
        verbose_name = _('issue reaction')
        verbose_name_plural = _('issue reactions')


class IssueMessage(models.Model):
    id = models.UUIDField(_('id'), primary_key=True, default=uuid.uuid4)
    created_at = models.DateTimeField(_('date created'), auto_now_add=True)
    updated_at = models.DateTimeField(_('date updated'), auto_now=True)
    is_archived = models.BooleanField(_('archive'), default=False)
    message = models.TextField(_('message'), blank=True)
    issue = models.ForeignKey(
        'main.Issue',
        verbose_name=_('issue'),
        on_delete=models.PROTECT
    )
    user = models.ForeignKey(
        'main.User',
        verbose_name=_('user'),
        on_delete=models.PROTECT
    )

    class Meta:
        ordering = ('-created_at', )
        verbose_name = _('issue message')
        verbose_name_plural = _('issue messages')


class IssueMessgeAttachment(models.Model):
    id = models.UUIDField(_('id'), primary_key=True, default=uuid.uuid4)
    created_at = models.DateTimeField(_('date created'), auto_now_add=True)
    is_archived = models.BooleanField(_('archive'), default=False)
    title = models.CharField(_('title'), max_length=64)
    url = models.URLField(_('url'))
    message = models.ForeignKey(
        'main.IssueMessage',
        verbose_name=_('message'),
        on_delete=models.PROTECT
    )
    user = models.ForeignKey(
        'main.User',
        verbose_name=_('user'),
        on_delete=models.PROTECT
    )

    class Meta:
        ordering = ('-created_at', )
        verbose_name = _('issue message attachment')
        verbose_name_plural = _('issue message attachments')


class IssueMessageMention(models.Model):
    id = models.UUIDField(_('id'), primary_key=True, default=uuid.uuid4)
    message = models.ForeignKey(
        'main.IssueMessage',
        verbose_name=_('message'),
        on_delete=models.PROTECT
    )
    user = models.ForeignKey(
        'main.User',
        verbose_name=_('user'),
        on_delete=models.PROTECT
    )

    class Meta:
        verbose_name = _('issue message mention')
        verbose_name_plural = _('issue message mentions')


class IssueMessageReaction(models.Model):
    id = models.UUIDField(_('id'), primary_key=True, default=uuid.uuid4)
    message = models.ForeignKey(
        'main.IssueMessage',
        verbose_name=_('message'),
        on_delete=models.PROTECT
    )
    user = models.ForeignKey(
        'main.User',
        verbose_name=_('user'),
        on_delete=models.PROTECT
    )
    reaction = models.CharField(_('reaction'), max_length=1)

    class Meta:
        verbose_name = _('issue message reaction')
        verbose_name_plural = _('issue message reactions')
