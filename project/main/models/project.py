import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

MEMBER_STATUS = (
    (0, _('admin')),
    (1, _('regular')),
    (2, _('outsider')),
    (3, _('temporary')),
)

PROJECT_PAYMENT_STATUS = (
    (0, _('paid')), # 支払い済（有効期限（支払いから1ヶ月）になると自動支払い）
    (1, _('temporary')), # お試し期間（有効期限（デフォルトで3ヶ月）の失効後、支払いなし）
    (2, _('canceled')), # 解約済（有効期限（支払いから1ヶ月）の失効後、支払いなし）
    (3, _('failed')), # 支払い失敗（有効期限（デフォルトで7日）の失効後、支払いなし）
    (3, _('no payment')), # 支払いなし
)


class Project(models.Model):
    id = models.UUIDField(_('id'), primary_key=True, default=uuid.uuid4)
    is_active = models.BooleanField(_('active'), default=True)
    created_at = models.DateTimeField(_('date created'), auto_now_add=True)
    updated_at = models.DateTimeField(_('date updated'), auto_now=True)
    user = models.ForeignKey(
        'main.User',
        verbose_name=_('user'),
        on_delete=models.PROTECT
    )
    name = models.CharField(_('name'), max_length=32)
    catchphrase = models.CharField(_('catchphrase'), max_length=64, blank=True)
    description = models.CharField(_('description'), max_length=512, blank=True)
    avatar_url = models.URLField(_('avatar_url'), blank=True)

    class Meta:
        ordering = ('-created_at', )
        verbose_name = _('project')
        verbose_name_plural = _('projects')

    def __str__(self):
        return self.name


class ProjectPayment(models.Model):
    id = models.UUIDField(_('id'), primary_key=True, default=uuid.uuid4)
    created_at = models.DateTimeField(_('date created'), auto_now_add=True)
    expired_at = models.DateTimeField(_('date expired'), blank=True, null=True)
    payment_id = models.CharField(_('payment id'), max_length=64, blank=True)
    price = models.IntegerField(_('price'), default=490)
    stage = models.IntegerField(_('stage'), choices=PROJECT_PAYMENT_STATUS)
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

    class Meta:
        ordering = ('-created_at', )
        verbose_name = _('project payment')
        verbose_name_plural = _('project payments')


class ProjectMember(models.Model):
    id = models.UUIDField(_('id'), primary_key=True, default=uuid.uuid4)
    created_at = models.DateTimeField(_('date created'), auto_now_add=True)
    updated_at = models.DateTimeField(_('date updated'), auto_now=True)
    status = models.IntegerField(_('status'), choices=MEMBER_STATUS)
    project = models.ForeignKey(
        'main.Project',
        verbose_name=_('project'),
        on_delete=models.PROTECT
    )
    user = models.ForeignKey(
        'main.User',
        verbose_name=_('user'),
        on_delete=models.PROTECT
    )

    class Meta:
        ordering = ('-updated_at', 'status')
        unique_together = ('project', 'user')
        verbose_name = _('project member')
        verbose_name_plural = _('project members')


class ProjectMessage(models.Model):
    id = models.UUIDField(_('id'), primary_key=True, default=uuid.uuid4)
    created_at = models.DateTimeField(_('date created'), auto_now_add=True)
    updated_at = models.DateTimeField(_('date updated'), auto_now=True)
    is_archived = models.BooleanField(_('archive'), default=False)
    message = models.TextField(_('message'))
    project = models.ForeignKey(
        'main.Project',
        verbose_name=_('project'),
        on_delete=models.PROTECT
    )
    user = models.ForeignKey(
        'main.User',
        verbose_name=_('user'),
        on_delete=models.PROTECT
    )

    class Meta:
        ordering = ('-created_at', )
        verbose_name = _('project message')
        verbose_name_plural = _('project messages')


class ProjectMessageAttachment(models.Model):
    id = models.UUIDField(_('id'), primary_key=True, default=uuid.uuid4)
    created_at = models.DateTimeField(_('date created'), auto_now_add=True)
    is_archived = models.BooleanField(_('archive'), default=False)
    title = models.CharField(_('title'), max_length=64)
    url = models.URLField(_('url'))
    message = models.ForeignKey(
        'main.ProjectMessage',
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
        verbose_name = _('project message attachment')
        verbose_name_plural = _('project message attachments')


class ProjectMessageMention(models.Model):
    id = models.UUIDField(_('id'), primary_key=True, default=uuid.uuid4)
    message = models.ForeignKey(
        'main.ProjectMessage',
        verbose_name=_('message'),
        on_delete=models.PROTECT
    )
    user = models.ForeignKey(
        'main.User',
        verbose_name=_('user'),
        on_delete=models.PROTECT
    )

    class Meta:
        verbose_name = _('project message mention')
        verbose_name_plural = _('project message mentions')


class ProjectMessageReaction(models.Model):
    id = models.UUIDField(_('id'), primary_key=True, default=uuid.uuid4)
    message = models.ForeignKey(
        'main.ProjectMessage',
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
        verbose_name = _('project message reaction')
        verbose_name_plural = _('project message reactions')
