import boto3
from config import MY_AWS_ACCESS_KEY, MY_AWS_SECRET_KEY, MY_AWS_REGION


def connect_s3():

    s3 = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=AWS_REGION
    )

    return s3