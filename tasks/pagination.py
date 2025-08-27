from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_query_param = "page"
    page_size_query_param = "page_size"

    def get_paginated_response(self, data):
        return Response({
            "data": data,
            "page": self.page.number,
            "limit": self.page.paginator.per_page,
            "total": self.page.paginator.count,
        })