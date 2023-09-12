from rest_framework import serializers
from admin_panel.model import static
from admin_panel.model import menu
from api.settings import serializers as menu_serializer

class StaticSerializer(serializers.ModelSerializer):

    class Meta:
        model = static.StaticPage
        fields = [
            'id', 'title', 'url', 'slug', 'views', 'active', 'content',
        ]


class StaticMenuSerializer(menu_serializer.HeaderSubMenuSerializer):
    class Meta:
        model = menu.Menu
        fields = [
            'id', 'title', 'url', 'is_static'
        ]
