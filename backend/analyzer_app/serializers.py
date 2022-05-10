from rest_framework import serializers
from .models import Video


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'


class VideoProcessSerializer(serializers.Serializer):
    progress = serializers.IntegerField()
    status = serializers.CharField(max_length=200)
