import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

USER_PLAN_PRICE = 490

GENDERS = (
    ('male', _('male')),      # 男性
    ('female', _('female')),  # 女性
    ('others', _('others')),  # その他の性別
    ('', _('not set'))        # 未設定
)

USER_PAYMENT_STATUS = (
    (0, _('paid')),        # 支払い済（有効期限（支払いから1ヶ月）になると自動支払い）
    (1, _('temporary')),   # お試し期間（有効期限（デフォルトで3ヶ月）の失効後、支払いなし）
    (2, _('canceled')),    # 解約済（有効期限（支払いから1ヶ月）の失効後、支払いなし）
    (3, _('failed')),      # 支払い失敗（有効期限（デフォルトで7日）の失効後、支払いなし）
    (3, _('no payment')),  # 支払いなし
)


class InactiveUser:
    username = 'unknown'
    is_active = False
    name = 'Unknown'

    def __init__(self, obj):
        self.id = obj['id']
        self.created_at = obj['created_at']


class User(models.Model):
    id = models.UUIDField(_('id'), primary_key=True, default=uuid.uuid4)
    username = models.CharField(_('username'), max_length=32, unique=True)
    is_active = models.BooleanField(_('active'), default=True)
    created_at = models.DateTimeField(_('date created'), auto_now_add=True)
    updated_at = models.DateTimeField(_('date updated'), auto_now=True)
    name = models.CharField(_('name'), max_length=32)
    short_bio = models.CharField(_('short_bio'), max_length=32, blank=True)
    bio = models.CharField(_('bio'), max_length=512, blank=True)
    avatar_url = models.URLField(_('avatar_url'), blank=True)
    gender = models.SlugField(_('gender'), choices=GENDERS, blank=True)
    birthday = models.DateField(_('birthday'), blank=True, null=True)

    class Meta:
        ordering = ('username', )
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.name

    def get_inactive_user(self):
        return InactiveUser(self)

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True


class UserPayment(models.Model):
    id = models.UUIDField(_('id'), primary_key=True, default=uuid.uuid4)
    created_at = models.DateTimeField(_('date created'), auto_now_add=True)
    expired_at = models.DateTimeField(_('date expired'), blank=True, null=True)
    payment_id = models.CharField(_('payment id'), max_length=64, blank=True)
    price = models.IntegerField(_('price'), default=USER_PLAN_PRICE)
    stage = models.IntegerField(_('stage'), choices=USER_PAYMENT_STATUS)
    user = models.ForeignKey(
        'main.User',
        verbose_name=_('user'),
        on_delete=models.PROTECT
    )

    class Meta:
        ordering = ('-created_at', )
        verbose_name = _('user payment')
        verbose_name_plural = _('user payments')


class UserConnection(models.Model):
    id = models.UUIDField(_('id'), primary_key=True, default=uuid.uuid4)
    created_at = models.DateTimeField(_('date created'), auto_now_add=True)
    updated_at = models.DateTimeField(_('date updated'), auto_now=True)
    bias = models.IntegerField(_('bias'), default=0)
    from_user = models.ForeignKey(
        'main.User',
        verbose_name=_('connected from'),
        on_delete=models.PROTECT,
        related_name='connections_to'
    )
    to_user = models.ForeignKey(
        'main.User',
        verbose_name=_('connected to'),
        on_delete=models.PROTECT,
        related_name='connections_from'
    )

    class Meta:
        ordering = ('-updated_at', '-bias')
        unique_together = ('from_user', 'to_user')
        verbose_name = _('user connection')
        verbose_name_plural = _('user connections')


class UserConnectionBlock(models.Model):
    id = models.UUIDField(_('id'), primary_key=True, default=uuid.uuid4)
    created_at = models.DateTimeField(_('date created'), auto_now_add=True)
    connection = models.ForeignKey(
        'main.UserConnection',
        verbose_name=_('connection'),
        on_delete=models.PROTECT
    )
    user = models.ForeignKey(
        'main.User',
        verbose_name=_('user'),
        on_delete=models.PROTECT
    )

    class Meta:
        ordering = ('-created_at', )
        unique_together = ('connection', 'user')
        verbose_name = _('user connection block')
        verbose_name_plural = _('user connections blocks')


class UserMessage(models.Model):
    id = models.UUIDField(_('id'), primary_key=True, default=uuid.uuid4)
    created_at = models.DateTimeField(_('date created'), auto_now_add=True)
    updated_at = models.DateTimeField(_('date updated'), auto_now=True)
    is_archived = models.BooleanField(_('archive'), default=False)
    message = models.TextField(_('message'))
    from_user = models.ForeignKey(
        'main.User',
        verbose_name=_('from'),
        on_delete=models.PROTECT,
        related_name='message_to'
    )
    to_user = models.ForeignKey(
        'main.User',
        verbose_name=_('to'),
        on_delete=models.PROTECT,
        related_name='message_from'
    )

    class Meta:
        ordering = ('-created_at', )
        verbose_name = _('user message')
        verbose_name_plural = _('user messages')


class UserMessageAttachment(models.Model):
    id = models.UUIDField(_('id'), primary_key=True, default=uuid.uuid4)
    created_at = models.DateTimeField(_('date created'), auto_now_add=True)
    is_archived = models.BooleanField(_('archive'), default=False)
    title = models.CharField(_('title'), max_length=64)
    url = models.URLField(_('url'))
    message = models.ForeignKey(
        'main.UserMessage',
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
        verbose_name = _('user message attachment')
        verbose_name_plural = _('user message attachments')


class UserMessageReaction(models.Model):
    id = models.UUIDField(_('id'), primary_key=True, default=uuid.uuid4)
    message = models.ForeignKey(
        'main.UserMessage',
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
        verbose_name = _('user message reaction')
        verbose_name_plural = _('user message reactions')
