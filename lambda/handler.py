import io
import boto3


def handler(event, context):
    for record in event['Records']:
        import cv2

        def video_duration(video_path):
            cap = cv2.VideoCapture(video_path)
            fps = cap.get(cv2.CAP_PROP_FPS)
            num_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
            duration_sec = int(num_frames / fps)
            return duration_sec
        duration = video_duration(record['location'])

        bucket_name = 'srawvideo'
        file_name = event['file_name']
        file = io.BytesIO(bytes(str(duration), encoding='utf-8'))
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(bucket_name)
        bucket_object = bucket.Object(file_name)
        bucket_object.upload_fileobj(file)
    return True
