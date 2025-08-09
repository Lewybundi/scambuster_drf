from rest_framework.pagination import PageNumberPagination

class ScamPostListPagination(PageNumberPagination):
    page_size = 2
    page_query_param = 'P'
    