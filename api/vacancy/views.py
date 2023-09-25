from django.utils.timezone import now
from rest_framework import viewsets, status, generics
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from admin_panel.model import ministry
from admin_panel.model import vacancy
from . import serializers
from .. import pagination


class AdmVacancyView(viewsets.ModelViewSet):
    queryset = vacancy.Vacancy.objects.all()
    serializer_class = serializers.VacancySerializer
    pagination_class = None
    http_method_names = ['get', 'post', 'put', 'delete']


class AdmEducationView(viewsets.ModelViewSet):
    queryset = vacancy.Education.objects.all()
    serializer_class = serializers.EducationSerializer
    pagination_class = None
    http_method_names = ['get', 'post', 'put', 'delete']


class AdmEmploymentView(viewsets.ModelViewSet):
    queryset = vacancy.Employment.objects.all()
    serializer_class = serializers.EmploymentSerializer
    pagination_class = None
    http_method_names = ['get', 'post', 'put', 'delete']
