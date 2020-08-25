import boto3
import time

from botocore.exceptions import ClientError

from fastapi import HTTPException
from app.core.config import settings


def upload_image_s3(file, content_type):
    s3 = boto3.resource(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

    time_millis = int(round(time.time() * 1000))
    filename = str(time_millis)+"."+content_type

    try:
        bucket = s3.Bucket(settings.AWS_S3_SITE_IMAGE_BUCKET)
        bucket.Object(filename).put(Body=file.file.read())
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=404,
            detail="Failed to upload image",
        )

    return filename


def create_pre_signed_url(object_name):
    s3_client = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

    try:
        url = s3_client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': settings.AWS_S3_SITE_IMAGE_BUCKET,
                'Key': object_name
            },
            ExpiresIn=settings.AWS_PRE_SIGNED_URL_EXPIRE_MINUTES)

    except ClientError as e:
        print(e)
        raise HTTPException(
            status_code=404,
            detail="Failed to upload image",
        )

    return url
