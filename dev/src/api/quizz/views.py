from django.db.models import F
from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response

from api import pagination
from . import serializers
from admin_panel.model import question


class CustomModalViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        queryset = self.queryset
        if hasattr(self.queryset.model, 'title'):
            queryset = self.queryset.exclude(title__exact='')
        
        return queryset
class QuizzListView(CustomModalViewSet):
    queryset = question.Quizz.objects.filter(is_published=True)
    serializer_class = serializers.QuizzSerializer
    pagination_class = pagination.ExtraShort
    http_method_names = ['get', 'post']

    def retrieve(self, request, *args, **kwargs):
        serializer = serializers.QuizzDetailSerializer
        # check if user already exists in question result model
        instance = self.get_object()
        payload = {
            'quizz': serializer(instance).data,
        }
        return Response(payload)

    @action(detail=True, methods=['post'])
    def answer(self, request, *args, **kwargs):
        data = self.request.data

        # ip = self.request.META
        instance = self.get_object()

        obj = question.QuestionResult.objects.create(question_id=data['question'], quizz=instance)
        # Increasing the answer count in the question
        question_instance = question.Question.objects.get(id=int(data['question']))
        question_instance.count += 1
        question_instance.save()
        payload = {
            'quizz': serializers.QuizzDetailSerializer(instance).data,
        }
        return Response(payload, status=status.HTTP_201_CREATED)


class QuizzView(QuizzListView):
    queryset = question.Quizz.objects.filter(main_page=True, is_published=True)
    pagination_class = None
    serializer_class = serializers.QuizzDetailSerializer

    def list(self, request, *args, **kwargs):
        instance = self.get_queryset().order_by('?').last()
        serializer = self.get_serializer_class()
        payload = {
            'quizz': serializer(instance).data,
        }
        return Response(payload)
