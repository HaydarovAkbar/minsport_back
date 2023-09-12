from rest_framework import serializers
from admin_panel.model import docs


class DocsSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = docs.Docs
        fields = [
            'id', 'title', 'date', 'issued_by', 'law', 'url', 'link'
        ]

    def get_url(self, obj):
        return obj.url if obj.url else obj.file_url

class DocTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = docs.DocType
        fields = [
            'id', 'title', 'slug',
        ]
