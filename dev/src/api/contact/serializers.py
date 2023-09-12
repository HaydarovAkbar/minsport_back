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
