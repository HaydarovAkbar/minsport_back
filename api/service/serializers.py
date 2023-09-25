from rest_framework import serializers
from admin_panel.model import service


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = service.Service
        fields = [
            'id', 'title', 'order', 'icon_url', 'url'
        ]


class AdmServiceSerializer(serializers.ModelSerializer):
    title_uz = serializers.CharField()
    title_ru = serializers.CharField()
    title_en = serializers.CharField()

    class Meta:
        model = service.Service
        fields = "__all__"


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
