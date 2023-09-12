from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from admin_panel.model import docs
from api import pagination
from . import serializers


class CustomModalViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        queryset = self.queryset
        if hasattr(self.queryset.model, 'title'):
            queryset = self.queryset.exclude(title__exact='')
        
        return queryset

class DocsListView(CustomModalViewSet):
    queryset = docs.Docs.objects.all()
    serializer_class = serializers.DocsSerializer
    pagination_class = pagination.ExtraMiddle
    http_method_names = ['get']
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['doc_type', 'doc_type__slug']

    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     docs = self.get_queryset().model
    #     for index, item in enumerate(range(1, 30)):
    #         asd = docs.objects.create(title=instance.title, issued_by=f"{instance.issued_by}-{index}", law=f"{instance.law}-{index}", doc_type=None, is_published=True)
    #
    #     return Response(self.serializer_class(instance).data, status=200)


class DocTypeView(CustomModalViewSet):
    queryset = docs.DocType.objects.all()
    serializer_class = serializers.DocTypeSerializer
    pagination_class = None
    http_method_names = ['get']
