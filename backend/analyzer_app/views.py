import os
from io import BytesIO
import boto3

from django.conf import settings
from rest_framework import viewsets, parsers, status
from rest_framework.decorators import action
from rest_framework.response import Response


from .models import Video
from .serializers import VideoSerializer, VideoProcessSerializer


class VideoViewset(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(detail=True, methods=['patch'])
    def update_progress(self, request, pk=None):
        user = self.get_object()
        serializer = VideoProcessSerializer(data=request.data)
        if serializer.is_valid():
            video = Video.objects.get(pk=pk)
            video.progress = serializer.validated_data.get('progress')
            if serializer.validated_data.get('status') == 'success':
                session = boto3.Session(profile_name=settings.AWS_S3_SESSION_PROFILE)
                s3_client = session.client("s3")
                f = BytesIO()
                s3_client.download_fileobj(settings.AWS_STORAGE_BUCKET_NAME, 'video_{0}/result.txt'.format(
                    os.path.basename(video.file_location.name)), f)
                result = f.getvalue()
                video.result = result
            video.save()
            return Response({'status': 'success'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
