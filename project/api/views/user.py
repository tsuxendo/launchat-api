from api.serializers import UserSerializer
from django_filters.rest_framework import DjangoFilterBackend
from main.models import User
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


class UserPermission(BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.method in ('POST', 'PATCH', 'DELETE') and
                    request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return bool(
            view.action in ('list', 'retrieve') or

            view.action in (
                'partial_update',
                'destroy'
            ) and request.user == obj and obj.is_active or

            view.action in (
                'connection_list',
                'message_list'
            ) and request.user.is_authenticated and obj.is_active or

            view.action in (
                'connection_block',
                'connection_unblock',
                'message_create',
                'message_destroy',
                'message_reaction',
            ) and obj.is_active
        )


class UserViewSet(ModelViewSet):
    """
    User
        list
            GET /users/
            search, ordering, cursor
        retrieve
            GET /users/<user.id>/
        partial_update
            PATCH /users/<user.id>/
        destroy
            DELETE /users/<user.id>/

    User Connection
        connection_list
            GET /users/<user.id>/connections/
            search, ordering, cursor
        connection_block
            POST /users/<user.id>/block/
        connection_unblock
            POST /users/<user.id>/unblock/

    User Message
        message_list
            GET /users/<user.id>/messages/
            search, cursor
        message_create
            POST /users/<user.id>/messages/
        message_delete
            DELETE /users/<user.id>/messages/<message.id>/
        message_reaction
            POST /users/<user.id>/messages/<message.id>/react/
    """
    filterset_fields = []
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    ordering = '-created_at'
    ordering_fields = ['created_at']
    permission_classes = [UserPermission]
    queryset = User.objects.all()
    search_fields = ['username', 'name', 'title', 'bio']
    serializer_class = UserSerializer

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

    def partial_update(self, request, *args, **kwargs):
        is_unkown = bool(
            request.data.get('username') == 'unknown' or
            request.data.get('name') == 'Unknown'
        )
        if is_unkown:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        if 'tags' in request.data:
            tags = request.data.get('tags').split(',')[:5]

        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)

    def perform_destroy(self, instance):

        # TODO
        # Transaction
        #     issue ごとまとめ、 message 以外の最新を取得、全て completed でなければ不可
        #     => 途中のものは完了させるように促すエラー
        # Project
        #     アーカイブされていないプロジェクトの所有者となっている場合は不可
        #     => プロジェクトの所有権を移動させるように促すエラー
        # Project Payment
        #     先に解約していなければ不可
        #     => フロント側で先に済んでいるはずなので不正リクエストエラー
        # User Payment
        #     先に解約していなければ不可
        #     => フロント側で先に済んでいるはずなので不正リクエストエラー

        import random, string, time

        random_string = ''.join(
            random.choices(string.ascii_letters + string.digits, k=6)
        )
        time_string = str(int(time.time()))
        instance.update(
            is_active=False,
            username=f'deleted_{random_string}_{time_string}',
            cognito_id=''
        )

    @action(methods=['GET'], detail=True, url_path='connections')
    def connection_list(self, request):
        # search, ordering, cursor
        pass

    @action(
        methods=['POST'],
        detail=True,
        url_path=r'connections/(?P<connection_id>\w+)/block/'
    )
    def connection_block(self, request, connection_id=None):
        pass

    @action(
        methods=['POST'],
        detail=True,
        url_path=r'connections/(?P<connection_id>\w+)/unblock/'
    )
    def connection_unblock(self, request, connection_id=None):
        pass

    @action(methods=['GET'], detail=True, url_path='messages')
    def message_list(self, request):
        # search, cursor
        pass

    @action(methods=['POST'], detail=True, url_path='messages')
    def message_create(self, request):
        pass

    @action(
        methods=['DELETE'],
        detail=True,
        url_path=r'messages/(?P<message_id>\w+)'
    )
    def message_destroy(self, request, message_id=None):
        pass

    @action(
        methods=['POST'],
        detail=True,
        url_path=r'messages/(?P<message_id>\w+)/react'
    )
    def message_reaction(self, request, message_id=None):
        pass
