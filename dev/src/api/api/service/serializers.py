from rest_framework import serializers
from admin_panel.model import service


class ServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = service.Service
        fields = [
            'id', 'title', 'order', 'icon_url', 'url'
        ]


class EmployeeRatingPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = service.EmployeeRating
        fields = [
            'id', 'region', 'district', 'organization', 'employee', 'service_type', 'grade_type'
        ]


class EmployeeRatingOverallSerializer(serializers.ModelSerializer):
    class Meta:
        model = service.EmployeeRating
        fields = [
            ''
        ]
