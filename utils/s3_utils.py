import boto3
from config import AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_REGION


def connect_s3():

    s3 = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=AWS_REGION
    )

    return s3