from rest_framework import serializers
from admin_panel.model import event
from api.views import RegionSerializer


class TagSerializer(serializers.RelatedField):
    def to_representation(self, value):
        obj = {
            'id': value.id,
            'title': value.title,
            'slug': value.slug,
        }
        return obj


class EventSerializer(serializers.ModelSerializer):
    region = serializers.CharField(source='region.title', required=False)
    type = serializers.CharField(source='type.title')

    # event_date = serializers.DateTimeField(format='%d %B %Y', required=False, read_only=True)

    class Meta:
        model = event.Event
        fields = [
            'id', 'title', 'views', 'description', 'address', 'event_place',
            'image_url', 'event_date', 'region', 'type', 'expired',
        ]


class EventDetailSerializer(EventSerializer):
    hashtag = TagSerializer(many=True, read_only=True)

    class Meta:
        model = event.Event
        fields = [
            'id', 'title', 'views', 'link', 'description', 'address', 'event_place',
            'image_url', 'event_date', 'region', 'type', 'expired', 'hashtag',
        ]


class IndexEventSerializer(serializers.ModelSerializer):
    # event_date = serializers.DateTimeField(format='%d %B %Y', required=False, read_only=True)
    region = serializers.CharField(source='region.title', required=False)

    class Meta:
        model = event.Event
        fields = [
            'id', 'title', 'event_place', 'image_url', 'event_date', 'description', 'region',
        ]
