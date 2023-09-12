
from django.utils.timezone import now
from rest_framework import viewsets, status, generics
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from admin_panel.model import ministry
from admin_panel.model import vacancy
from . import serializers
from .. import pagination


class CustomModalViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        queryset = self.queryset
        if hasattr(self.queryset.model, 'title'):
            queryset = self.queryset.exclude(title__exact='')
        
        return queryset



class AboutUsView(CustomModalViewSet):
    queryset = ministry.AboutMinistry.objects.all()
    serializer_class = serializers.AboutUsSerializer
    pagination_class = None
    http_method_names = ['get']

    def list(self, request):
        stat = serializers.StatSerializer(ministry.MinistryStat.objects.all(), many=True).data
        about = serializers.AboutUsSerializer(self.get_queryset(), many=True).data
        dict = {
            'about': about,
            'stat': stat,
        }
        return Response(dict, status=status.HTTP_200_OK)


class StructureView(CustomModalViewSet):
    queryset = ministry.MinistryStructure.objects.all()
    serializer_class = serializers.StructureSerializer
    pagination_class = None
    http_method_names = ['get']


class VacancyView(CustomModalViewSet):
    # sending vacancy in the company
    queryset = vacancy.Vacancy.objects.all().filter(is_published=True).order_by(
        '-date')
    serializer_class = serializers.VacancySerializer
    pagination_class = None
    http_method_names = ['get']


class StaffView(CustomModalViewSet):
    # sending only leaders in the company
    queryset = ministry.Staff.objects.all().filter(leader=True, is_central=False)
    serializer_class = serializers.StaffSerializer
    pagination_class = None
    http_method_names = ['get']


class StaffRegionView(CustomModalViewSet):
    queryset = ministry.Staff.objects.all().filter(leader=False, is_central=False, department__isnull=False)
    serializer_class = serializers.StaffRegionalSerializer
    pagination_class = None
    http_method_names = ['get']


class StaffOrganizationView(CustomModalViewSet):
    queryset = ministry.Staff.objects.all().filter(leader=False, is_central=False, organization__isnull=False)
    serializer_class = serializers.StaffOrganizationSerializer
    pagination_class = None
    http_method_names = ['get']


class StaffCentralView(CustomModalViewSet):
    queryset = ministry.Staff.objects.all().filter(is_central=True, leader=False)
    serializer_class = serializers.StaffCentralSerializer
    pagination_class = None
    http_method_names = ['get']


class AllDepartmentView(CustomModalViewSet, generics.ListAPIView):
    queryset = ministry.Department.objects.all()
    serializer_class = serializers.DepartmentSerializer
    pagination_class = None
    http_method_names = ['get']
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['title_uz', 'title_ru', 'title_en', ]
    filterset_fields = ['region']

    def list(self, request, *args, **kwargs):
        instance = self.get_queryset()
        organization_instance = ministry.Organization.objects.all()

        department_serializer = self.serializer_class
        organization_serializer = serializers.OrganizationSerializer

        context = {
            "request": request,
        }
        department = department_serializer(instance, many=True, context=context)
        organization = organization_serializer(organization_instance, many=True, context=context)

        response = department.data + organization.data
        return Response(response)


class DepartmentView(CustomModalViewSet, generics.ListAPIView):
    """Included both viewset and generic. Search and Filter are not properly supported in viewset only"""
    queryset = ministry.Department.objects.all()
    serializer_class = serializers.DepartmentSerializer
    pagination_class = None
    http_method_names = ['get']
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['title_uz', 'title_ru', 'title_en', ]
    filterset_fields = ['region']


    # def get_queryset(self):
    #     queryset = self.get_queryset()
    #     # Filter: category ID in request params
    #     category = self.request.GET.get('category', None)
    #     if category is not None:
    #         queryset = queryset.filter(category=category)
    #     return queryset


class OrganizationView(DepartmentView):
    queryset = ministry.Organization.objects.all()
    serializer_class = serializers.OrganizationListSerializer
    pagination_class = None
    http_method_names = ['get']
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['region', 'region__title', 'district', 'district__title']

    def get_serializer_class(self):
        if self.action == 'list':
            return self.serializer_class
        else:
            return serializers.OrganizationDetailSerializer
