from rest_framework import serializers
from admin_panel.model import tender


class TenderSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='type.title', required=False, read_only=True)
    primary_color = serializers.CharField(source='type.primary', required=False, read_only=True)
    region = serializers.CharField(source='region.title')

    class Meta:
        model = tender.Tender
        fields = [
            'id', 'title', 'date', 'number', 'organizer', 'file_url',
            'type', 'primary_color', 'region'
        ]
