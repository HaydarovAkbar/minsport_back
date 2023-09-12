from itertools import chain

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, filters
from admin_panel.model import event, press_service, static, question
from . import serializers


class Search(APIView):

    # filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    # search_fields = [filters.SearchFilter]

    def post(self, request):
        # lang_code = request.LANGUAGE_CODE
        print(self.request.POST, 'POST')
        query = self.request.POST.get('query')
        events = event.Event.objects.filter(title__icontains=query)
        quizz = question.Quizz.objects.filter(title__icontains=query)
        news = press_service.News.objects.filter(title__icontains=query)
        photogallery = press_service.PhotoGallery.objects.filter(title__icontains=query)
        videogallery = press_service.VideoGallery.objects.filter(title__icontains=query)
        static_page = static.StaticPage.objects.filter(title__icontains=query)
        results = chain(events, events, news, photogallery, videogallery, static_page,)

        serializer = serializers.SearchSerializer(
            {'events': events, 'quizz': quizz, 'news': news, 'photogallery': photogallery,
             'videogallery': videogallery, 'static_page': static_page}, context={'request': request})
        return Response(data=serializer.data)


class ImageUploadView(generics.CreateAPIView):
    queryset = press_service.MediaImage.objects.all()
    serializer_class = serializers.MediaImageSerializer
    permission_classes = [IsAuthenticated]


