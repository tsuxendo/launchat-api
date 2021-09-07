from django.contrib.admin.decorators import register
from .models import (
    Hashtag,
    UserTag,
    IssueTag,
    ProjectTag,

    Issue,
    IssueAttachment,
    IssueMention,
    IssueReaction,
    IssueMessage,
    IssueMessgeAttachment,
    IssueMessageMention,
    IssueMessageReaction,

    Notification,

    Project,
    ProjectPayment,
    ProjectMember,
    ProjectMessage,
    ProjectMessageAttachment,
    ProjectMessageMention,
    ProjectMessageReaction,

    TimelineItem,

    Transaction,
    TransactionAttachment,

    User,
    UserPayment,
    UserConnection,
    UserConnectionBlock,
    UserMessage,
    UserMessageAttachment,
    UserMessageReaction,
)
from django.contrib import admin


admin.site.register(Hashtag)
admin.site.register(UserTag)
admin.site.register(IssueTag)
admin.site.register(ProjectTag)

admin.site.register(Issue)
admin.site.register(IssueAttachment)
admin.site.register(IssueMention)
admin.site.register(IssueReaction)
admin.site.register(IssueMessage)
admin.site.register(IssueMessgeAttachment)
admin.site.register(IssueMessageMention)
admin.site.register(IssueMessageReaction)

admin.site.register(Notification)

admin.site.register(Project)
admin.site.register(ProjectPayment)
admin.site.register(ProjectMember)
admin.site.register(ProjectMessage)
admin.site.register(ProjectMessageAttachment)
admin.site.register(ProjectMessageMention)
admin.site.register(ProjectMessageReaction)

admin.site.register(TimelineItem)

admin.site.register(Transaction)
admin.site.register(TransactionAttachment)

admin.site.register(User)
admin.site.register(UserPayment)
admin.site.register(UserConnection)
admin.site.register(UserConnectionBlock)
admin.site.register(UserMessage)
admin.site.register(UserMessageAttachment)
admin.site.register(UserMessageReaction)
