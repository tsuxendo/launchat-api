from rest_framework.pagination import CursorPagination


class CursorPagination(CursorPagination):
    cursor_query_param = 'cursor'
    max_page_size = 100
    ordering = '-created_at'
    page_size = 10
    page_size_query_param = 'page_size'
