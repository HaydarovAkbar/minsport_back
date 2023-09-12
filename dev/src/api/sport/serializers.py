from rest_framework import serializers
from admin_panel.model import sport


class StadionSerializer(serializers.ModelSerializer):
    region = serializers.CharField(source='region.title', required=False, read_only=True)

    class Meta:
        model = sport.Stadion
        fields = [
            'id', 'title', 'description', 'address',
            'region', 'host_team', 'established', 'capacity', 'image_url',
        ]


class ChampionSerializer(serializers.ModelSerializer):
    sport = serializers.CharField(source='sport.title', read_only=True, required=False)

    class Meta:
        model = sport.Champion
        fields = [
            'id', 'title', 'sport', 'competition',
            'image_url', 'medal', 'description',
        ]
