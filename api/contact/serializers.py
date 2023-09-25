from rest_framework import serializers
from admin_panel.model import contact
from api.about.serializers import StaffSerializer


class ContactTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = contact.ContactType
        fields = [
            'id', 'title'
        ]


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = contact.Contact
        fields = [
            'sender_name', 'type', 'email', 'message', 'image'
        ]


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = contact.Feedback
        fields = [
            'sender_name', 'topic', 'email', 'message'
        ]


class ReceptionSerializer(serializers.ModelSerializer):
    day = serializers.CharField(source='day.title', required=False)
    staff = serializers.CharField(source='staff.title', required=False)
    position = serializers.SerializerMethodField()

    class Meta:
        model = contact.Reception
        fields = [
            'id', 'staff', 'position', 'day', 'time',
        ]

    def get_position(self, obj):
        if obj.staff:
            return obj.staff.position


class StatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = contact.Feedback
        fields = [
            'sender_name', 'topic', 'email', 'message'
        ]


class AdmContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = contact.Contact
        fields = '__all__'


class AdmReceptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = contact.Reception
        fields = '__all__'


    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['day_title_uz'] = instance.day.title_uz
        response['day_title_ru'] = instance.day.title_ru
        response['day_title_en'] = instance.day.title_en
        response['staff_title_uz'] = instance.staff.title_uz
        response['staff_title_ru'] = instance.staff.title_ru
        response['staff_title_en'] = instance.staff.title_en
        return response


class AdmWeekDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = contact.WeekDay
        fields = '__all__'