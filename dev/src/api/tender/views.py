from django.utils import timezone
from rest_framework import viewsets
from . import serializers
from admin_panel.model import tender
from api import pagination

class CustomModalViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        queryset = self.queryset
        if hasattr(self.queryset.model, 'title'):
            queryset = self.queryset.exclude(title__exact='')
        
        return queryset
class TenderListView(CustomModalViewSet):
    queryset = tender.Tender.objects.filter(is_published=True).order_by(
        '-date')
    serializer_class = serializers.TenderSerializer
    pagination_class = None
    http_method_names = ['get']
