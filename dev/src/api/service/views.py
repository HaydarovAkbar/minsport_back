from rest_framework import viewsets
from rest_framework.response import Response
from django.db.models import Count, Avg

from admin_panel.model import service
from admin_panel.model.service import EmployeeRating
from rest_framework.decorators import action
from . import serializers


class CustomModalViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        queryset = self.queryset
        if hasattr(self.queryset.model, 'title'):
            queryset = self.queryset.exclude(title__exact='')

        return queryset


class ServiceListView(CustomModalViewSet):
    queryset = service.Service.objects.all()
    serializer_class = serializers.ServiceSerializer
    pagination_class = None
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        instance = self.get_queryset()
        more = self.get_queryset().count() > 6
        serializer = self.serializer_class
        payload = {
            'more': more,
            'services': serializer(instance, many=True).data,
        }

        return Response(payload)


class EmployeeRatingModalViewSet(CustomModalViewSet):
    queryset = service.EmployeeRating.objects.all()
    serializer_class = serializers.EmployeeRatingPostSerializer
    pagination_class = None
    http_method_names = ['get', 'post']

    @action(detail=False, methods=['get'])
    def summary(self, request):
        service_types = self.queryset.values('service_type') \
                            .annotate(total_count=Count('id'),
                                      avg_grade=Avg('grade_type')) \
                            .order_by('-total_count', '-avg_grade')[:3]
        service_summary = []
        for service in service_types:
            service_name = dict(EmployeeRating.service_choice).get(service['service_type'])
            service_summary.append({'service_type': service_name,
                                    'total_count': service['total_count'],
                                    'avg_grade': round(service['avg_grade'], 1)})
        return Response(service_summary)
