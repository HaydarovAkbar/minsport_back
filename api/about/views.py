from django.utils.timezone import now
from rest_framework import viewsets, status, generics
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from admin_panel.model import ministry
from admin_panel.model import vacancy
from . import serializers
from .. import pagination
from datetime import datetime, timedelta
from django.utils.timezone import make_aware


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
        organization_serializer = serializers.OrganizationListSerializer

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


class AdmAboutMinistryView(viewsets.ModelViewSet):
    queryset = ministry.AboutMinistry.objects.all()
    serializer_class = serializers.AdmAboutMinistrySerializer
    pagination_class = None
    http_method_names = ['get', 'post', 'put', 'delete']


class AdmMinistryStructureView(viewsets.ModelViewSet):
    queryset = ministry.MinistryStructure.objects.all().order_by('-id')
    serializer_class = serializers.AdmMinistryStructureSerializer
    pagination_class = None
    http_method_names = ['get', 'post', 'put', 'delete']


class AdmMinistryStatView(viewsets.ModelViewSet):
    queryset = ministry.MinistryStat.objects.all()
    serializer_class = serializers.AdmMinistryStatSerializer
    pagination_class = None
    http_method_names = ['get', 'post', 'put', 'delete']


class AdmMinistryStaffView(viewsets.ModelViewSet):
    queryset = ministry.Staff.objects.all()
    serializer_class = serializers.AdmMinistryStaffSerializer
    pagination_class = pagination.CustomPagination
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_queryset(self):
        main = self.request.query_params.get('main', None)
        leader = self.request.query_params.get('leader', None)
        department = self.request.query_params.get('department', None)
        organization = self.request.query_params.get('organization', None)
        is_central = self.request.query_params.get('is_central', None)
        params = self.request.query_params.get('params', None)
        q = self.request.query_params.get('q', None)
        filters = {}
        if main:
            filters['main'] = True if main == 'true' else False
        if leader:
            filters['leader'] = True if leader == 'true' else False
        if department:
            filters['department__isnull'] = False
        if organization:
            filters['organization__isnull'] = False
        if is_central:
            filters['is_central'] = True if is_central == 'true' else False
        if params:
            if q and params == 'title':
                filters['title__icontains'] = q
            if q and params == 'position':
                filters['position__icontains'] = q
            if q and params == 'organization':  # organization title
                filters['organization__title__icontains'] = q
        return self.queryset.filter(**filters)


class AdmMinistryDepartmentView(viewsets.ModelViewSet):
    queryset = ministry.Department.objects.all()
    serializer_class = serializers.AdmMinistryDepartmentSerializer
    pagination_class = pagination.CustomPagination
    http_method_names = ['get', 'post', 'put', 'delete']


class AdmMinistryOrganizationView(viewsets.ModelViewSet):
    queryset = ministry.Organization.objects.all()
    serializer_class = serializers.AdmMinistryOrganizationSerializer
    pagination_class = pagination.CustomPagination
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_queryset(self):
        region = self.request.query_params.get('region', None)
        district = self.request.query_params.get('district', None)
        params = self.request.query_params.get('params', None)
        q = self.request.query_params.get('q', None)
        filters = {}
        if region:
            filters['region__id'] = region
        if district:
            filters['district__id'] = district
        if params:
            if q and params == 'title':
                filters['title__icontains'] = q
            if q and params == 'address':
                filters['address__icontains'] = q
        return self.queryset.filter(**filters)


class VisitorView(viewsets.ModelViewSet):
    queryset = ministry.Visitor.objects.all()
    serializer_class = serializers.VisitorSerializer
    pagination_class = None
    http_method_names = ['get', 'post', 'put', 'delete']

    def list(self, request, *args, **kwargs):
        try:
            date_from = request.query_params.get('date_from', None)
            date_to = request.query_params.get('date_to', None)
            if date_from and date_to:
                date_from = datetime.strptime(date_from, '%Y-%m-%d')
                date_to = datetime.strptime(date_to, '%Y-%m-%d') + timedelta(days=1)
                date_from = make_aware(date_from)
                # date_to = make_aware(date_to)
                last_week = datetime.now() - timedelta(days=7)
                # last_week = make_aware(last_week)
                last_week_visitor_count = ministry.VisitorLog.objects.filter(
                    created_at__range=[last_week, datetime.now()]).count()
                last_month = datetime.now() - timedelta(days=30)
                # last_month = make_aware(last_month)
                last_month_visitor_count = ministry.VisitorLog.objects.filter(
                    created_at__range=[last_month, datetime.now()]).count()
                last_year = datetime.now() - timedelta(days=365)
                # last_year = make_aware(last_year)
                last_year_visitor_count = ministry.VisitorLog.objects.filter(
                    created_at__range=[last_year, datetime.now()]).count()
                result = ministry.VisitorLog.objects.filter(created_at__range=[date_from, date_to])
                count = result.count()
                return Response({'status': True, 'result_count': count,
                                 'last_week_visitor_count': last_week_visitor_count,
                                 'last_month_visitor_count': last_month_visitor_count,
                                 'last_year_visitor_count': last_year_visitor_count}, status=status.HTTP_200_OK)
        except Exception:
            return Response({'status': False}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        try:
            user_agent = request.data['browser']
            ip = request.data['ip']
            if user_agent:
                if_user = self.queryset.filter(browser=user_agent)
                if not if_user:
                    if_user = self.queryset.create(browser=user_agent, ip=ip, device=request.data['device'],
                                                   os=request.data['os'])
                else:
                    if_user = if_user.first()
            current_datetime = datetime.now().date()
            # year = current_datetime.year
            # month = current_datetime.month
            # day = current_datetime.day
            result = ministry.VisitorLog.objects.filter(visitor=if_user, created_at__date=current_datetime)
            # print(result)
            if not result:
                ministry.VisitorLog.objects.create(visitor=if_user, url=request.data['ip'])
            count = ministry.VisitorLog.objects.filter(created_at__date=current_datetime).count()
            return Response({'count': count, 'status': True}, status=status.HTTP_200_OK)
        except Exception:
            return Response({'status': False}, status=status.HTTP_400_BAD_REQUEST)

    # def retrieve(self, request, *args, **kwargs):
    #     try:
    #         date_from = request.query_params.get('date_from', None)
    #         date_to = request.query_params.get('date_to', None)
    #         if date_from and date_to:
    #             date_from = datetime.strptime(date_from, '%Y-%m-%d')
    #             date_to = datetime.strptime(date_to, '%Y-%m-%d') + timedelta(days=1)
    #             date_from = make_aware(date_from)
    #             date_to = make_aware(date_to)
    #             last_week = datetime.now() - timedelta(days=7)
    #             last_week = make_aware(last_week)
    #             last_week_visitor_count = ministry.VisitorLog.objects.filter(
    #                 created_at__range=[datetime.now(), last_week]).count()
    #             last_month = datetime.now() - timedelta(days=30)
    #             last_month = make_aware(last_month)
    #             last_month_visitor_count = ministry.VisitorLog.objects.filter(
    #                 created_at__range=[datetime.now(), last_month]).count()
    #             last_year = datetime.now() - timedelta(days=365)
    #             last_year = make_aware(last_year)
    #             last_year_visitor_count = ministry.VisitorLog.objects.filter(
    #                 created_at__range=[datetime.now(), last_year]).count()
    #             result = ministry.VisitorLog.objects.filter(created_at__range=[date_from, date_to])
    #             count = result.count()
    #             return Response({'status': True, 'result_count': count,
    #                              'last_week_visitor_count': last_week_visitor_count,
    #                              'last_month_visitor_count': last_month_visitor_count,
    #                              'last_year_visitor_count': last_year_visitor_count}, status=status.HTTP_200_OK)
    #     except Exception:
    #         return Response({'status': False}, status=status.HTTP_400_BAD_REQUEST)


class StaffListView(viewsets.ModelViewSet):
    queryset = ministry.Staff.objects.all()
    serializer_class = serializers.AdmMinistryStaffSerializer
    pagination_class = pagination.CustomPagination
    http_method_names = ['get', ]

    def get_queryset(self):
        main = self.request.query_params.get('main', None)
        leader = self.request.query_params.get('leader', None)
        department = self.request.query_params.get('department', None)
        organization = self.request.query_params.get('organization', None)
        is_central = self.request.query_params.get('is_central', None)
        filters = {}
        if main:
            filters['main'] = True if main == 'true' else False
        if leader:
            filters['leader'] = True if leader == 'true' else False
        if department:
            filters['department__isnull'] = False
        if organization:
            filters['organization__isnull'] = False
        if is_central:
            filters['is_central'] = True if is_central == 'true' else False
        return self.queryset.filter(**filters)
