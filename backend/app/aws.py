import os

import boto3

s3_resource = boto3.resource('s3',
                             aws_access_key_id=os.environ.get(
                                 "AWS_SERVER_PUBLIC_KEY"),
                             aws_secret_access_key=os.environ.get(
                                 "AWS_SERVER_SECRET_KEY"),
                             region_name=os.environ.get("REGION_NAME")
                             )
