from rest_framework.pagination import CursorPagination

class Mycustompagination(CursorPagination):
    page_size=3
    ordering = 'id'
    cursor_query_param='cu'  