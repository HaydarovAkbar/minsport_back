from rest_framework import serializers
from rest_framework.reverse import reverse
from admin_panel.model import press_service
from django.conf import settings


class TagSerializer(serializers.RelatedField):
    def to_representation(self, value):
        obj = {
            'id': value.id,
            'title': value.title,
            'slug': value.slug,
        }
        return obj


class NewsListSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.title', required=False)
    category_slug = serializers.CharField(source='category.slug', required=False)

    class Meta:
        model = press_service.News
        fields = [
            'id', 'title', 'views', 'thumbnail_url', 'publish_date',
            'category', 'category_slug', 'actual'
        ]


class NewsTopSerializer(NewsListSerializer):
    thumbnail_url = serializers.CharField(source='cover_url')


class HeaderNewsSerializer(NewsListSerializer):
    class Meta:
        model = press_service.News
        fields = [
            'id', 'title'
        ]


class NewsDetailSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.title', required=False)
    hashtag = TagSerializer(many=True, read_only=True)

    class Meta:
        model = press_service.News
        fields = [
            'id', 'title', 'description', 'short_description', 'image_url', 'views', 'publish_date',
            'category', 'hashtag',
        ]


class NewsCategoryserializer(serializers.ModelSerializer):
    class Meta:
        model = press_service.NewsCategory
        fields = ['id', 'title', 'order', 'slug']


class NewsHashtagserializer(serializers.ModelSerializer):
    class Meta:
        model = press_service.NewsHashtag
        fields = ['id', 'title', 'slug']


class PressSerializer(serializers.ModelSerializer):
    press = serializers.SerializerMethodField()

    class Meta:
        model = press_service.PressArticleLink
        fields = [
            'id', 'title', 'language', 'link', 'publish_date', 'press',
        ]

    def get_press(self, obj):
        if obj.press:
            payload = {
                'title': obj.press.title,
                'link': obj.press.link,
                'icon': obj.press.icon_url,
            }
            return payload


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = press_service.FAQ
        fields = [
            'id', 'title', 'description',
        ]


class NewsIntegration(serializers.Serializer):
    id = serializers.IntegerField()
    post_id = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    created = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    text = serializers.SerializerMethodField()
    reactions = serializers.SerializerMethodField()
    reach = serializers.SerializerMethodField()
    impressions = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()

    def get_post_id(self, obj):
        return obj.id
    
    def get_type(self, obj):
        return ''

    def get_created(self, obj):
        return obj.created_at
    
    def get_url(self, obj):
        frontend = 'https://minsport.uz/news/post/'
        url = frontend + str(obj.id)
        return url

    def get_text(self, obj):
        return obj.short_description

    def get_reactions(self, obj):
        return {
            "reactions": 0,
            "likes": 0,
            "views": obj.views,
            "comments": 0,
            "reposts": 0,
            "fallowers": 0,
        }
    
    def get_reach(self, obj):
        return {}
    
    def get_impressions(self, obj):
        return {}
    
    def get_categories(self, obj):
        return []