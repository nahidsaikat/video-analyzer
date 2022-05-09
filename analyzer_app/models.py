from django.db import models


def upload_to_path(instance, filename):
    return 'video_{0}/{1}'.format(filename, filename)


class Video(models.Model):
    progress = models.IntegerField(blank=True, null=True)
    result = models.IntegerField(blank=True, null=True)
    file_location = models.FileField(max_length=30, upload_to=upload_to_path)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Videos'
