from django.db import models


class Video(models.Model):
    progress = models.IntegerField(blank=True, null=True)
    result = models.IntegerField(blank=True, null=True)
    file_location = models.FileField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Videos'
