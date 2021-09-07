import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

TRANSACTION_STAGE = (
    (0, _('issued')), # 発行済ステージ（取引の条件など変更可能）
    (1, _('agreed')), # 合意済ステージ（契約書の発行、委託者は期限（デフォルトで14日以内）までに仮払いを済ませ、仮払いステージへ進む必要あり）
    (2, _('temporarily paid')), # 仮払い済ステージ（受託者は期日までに提出を済ませ、提出ステージへ進む必要あり）
    (3, _('submitted')), # 提出済ステージ（委託者は期限（デフォルトで7日以内）までに評価を済ませ、評価ステージへ進む必要あり）
    (4, _('valuated')), # 評価済ステージ（委託者は提出物などに応じて評価する、一部の取引の条件など変更可能。委託者と受託者は評価の承諾・不承諾を済ませ、承諾ステージへ進む必要あり）
    (5, _('approved')), # 承諾済ステージ（承諾・不承諾に応じて支払いまたは払い戻しが行われ、完了ステージへ。結果に応じて請求書、領収書の発行）
    (6, _('completed')), # 完了済ステージ
)

TRANSACTION_METHODS = (
    (0, _('issue')), # 発行
    (1, _('editing')), # 編集
    (2, _('agreement')), # 合意
    (3, _('temporary advance')), # 仮払い
    (4, _('reporting of work start')), # 勤務開始報告
    (5, _('reporting of work end')), # 勤務終了報告
    (6, _('submission')), # 提出
    (7, _('valuation')), # 評価
    (8, _('revaluation')), # 再評価
    (9, _('approval')), # 承諾
    (10, _('disapproval')), # 不承諾
    (11, _('payment')), # 支払い
    (12, _('refund')), # 払い戻し
    (13, _('message')), # メッセージ送信
)


class Transaction(models.Model):
    id = models.UUIDField(_('id'), primary_key=True, default=uuid.uuid4)
    created_at = models.DateTimeField(_('date created'), auto_now_add=True)
    deadlined_at = models.DateTimeField(_('date deadlined'), blank=True, null=True)
    payment_id = models.CharField(_('payment id'), max_length=64, blank=True)
    stage = models.IntegerField(_('stage'), choices=TRANSACTION_STAGE)
    method = models.IntegerField(_('method'), choices=TRANSACTION_METHODS)
    price = models.IntegerField(_('price'))
    message = models.TextField(_('message'), blank=True)
    client = models.ForeignKey(
        'main.User',
        verbose_name=_('client'),
        on_delete=models.PROTECT,
        related_name='request_transaction',
        null=True
    )
    worker = models.ForeignKey(
        'main.User',
        verbose_name=_('worker'),
        on_delete=models.PROTECT,
        related_name='worked_transaction'
    )
    issue = models.ForeignKey(
        'self',
        verbose_name=_('mention'),
        on_delete=models.PROTECT,
        null=True
    )

    class Meta:
        ordering = ('-created_at', )
        verbose_name = _('transaction')
        verbose_name_plural = _('transactions')


class TransactionAttachment(models.Model):
    id = models.UUIDField(_('id'), primary_key=True, default=uuid.uuid4)
    created_at = models.DateTimeField(_('date created'), auto_now_add=True)
    is_archived = models.BooleanField(_('archive'), default=False)
    title = models.CharField(_('title'), max_length=64)
    url = models.URLField(_('url'))
    transaction = models.ForeignKey(
        'main.Transaction',
        verbose_name=_('transaction'),
        on_delete=models.PROTECT
    )
    user = models.ForeignKey(
        'main.User',
        verbose_name=_('user'),
        on_delete=models.PROTECT
    )

    class Meta:
        ordering = ('-created_at', )
        verbose_name = _('transaction attachment')
        verbose_name_plural = _('transaction attachments')
