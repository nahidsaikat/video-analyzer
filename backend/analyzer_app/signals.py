from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Video
from .tasks import sqnd_sqs_message_task


@receiver(post_save, sender=Video)
def trigger_lambda(sender, instance, created, **kwargs):
    if created:
        sqnd_sqs_message_task.delay(instance)
