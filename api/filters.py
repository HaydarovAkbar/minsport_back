# from rest_framework.filters import BaseFilterBackend
#
#
# class CategoryFilter(BaseFilterBackend):
#     """
#     Filter that only allows users to see their own objects.
#     """
#     def filter_queryset(self, request, queryset, view):
#         param = request.QUERY_PARAMS.get('category', None)
#         if param is not None:
#             return queryset.filter(category=param)
#         return queryset
import django_filters
from django_filters import filters

from admin_panel.model import event


class CustomDateFilter(filters.Filter):
    date_time = django_filters.DateTimeFilter(name="date_time", lookup_expr='gte')