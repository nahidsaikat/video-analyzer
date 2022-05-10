import io
import os
import boto3
import json
import time
import requests


def handler(event, context):
    for record in event['Records']:
        import cv2

        data = json.loads(record['body'])
        base_api = os.environ['backend_base_api_url']
        url = base_api + '/videos/' + data['video_id'] + '/update_progress/'
        counter = 1
        starttime = time.time()
        while counter < 100:
            requests.patch(url, data={'progress': counter, 'status': 'in-progress'})
            time.sleep(60.0 - ((time.time() - starttime) % 60.0))
            counter += 1

        def video_duration(video_path):
            cap = cv2.VideoCapture(video_path)
            fps = cap.get(cv2.CAP_PROP_FPS)
            num_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
            duration_sec = int(num_frames / fps)
            return duration_sec
        duration = video_duration(data['location'])

        bucket_name = 'srawvideo'
        file_name = data['file_name']
        file = io.BytesIO(bytes(str(duration), encoding='utf-8'))
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(bucket_name)
        bucket_object = bucket.Object(file_name)
        bucket_object.upload_fileobj(file)

        requests.patch(url, data={'progress': counter, 'status': 'success'})
    return True
