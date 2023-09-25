from rest_framework import serializers
from admin_panel.model import menu, static
from django.conf import settings
from django.db.models import Count, Avg


class AdmMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = menu.Menu
        fields = '__all__'


class AdmStaticPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = static.StaticPage
        fields = '__all__'