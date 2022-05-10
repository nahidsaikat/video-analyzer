from celery import shared_task

import json
import boto3
from botocore.exceptions import ClientError
from django.conf import settings


@shared_task
def sqnd_sqs_message_task(video):
    session = boto3.Session(profile_name=settings.AWS_S3_SESSION_PROFILE)
    sqs = session.client("sqs")
    queue = sqs.get_queue_by_name(QueueName=settings.AWS_SQS_NAME)
    try:
        data = {
            'location': video.file_location.url,
            'file_name': video.file_location.name
        }
        response = queue.send_message(
            MessageBody=json.dumps(data),
            MessageAttributes={}
        )
    except ClientError as error:
        raise error
    else:
        return response
