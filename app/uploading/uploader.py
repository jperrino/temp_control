import boto3
from app.config import common_settings

'''
    AWS CONFIGURATION
'''
AWS_ACCESS_KEY = common_settings.aws_access_key
AWS_SECRET_KEY = common_settings.aws_secret_key
AWS_BUCKET_NAME = common_settings.aws_bucket_name
AWS_URL = common_settings.aws_url

s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)


def upload_graph_to_s3_bucket(file_path: str, file_key: str):
    with open(file_path, 'rb') as file:
        s3_client.upload_fileobj(file, AWS_BUCKET_NAME, file_key)

    file_s3_url = AWS_URL.replace('{bucket_name}', AWS_BUCKET_NAME).replace('{s3_key}', file_key)

    bucket_location = s3_client.get_bucket_location(Bucket=AWS_BUCKET_NAME)['LocationConstraint']
    if bucket_location is None:
        file_s3_url = file_s3_url.replace('{bucket_location}', '')
        # url = f"https://s3.amazonaws.com/{AWS_BUCKET_NAME}/{s3_key}"
    else:
        file_s3_url = file_s3_url.replace('{bucket_location}', "-" + bucket_location)
        # url = f"https://s3-{bucket_location}.amazonaws.com/{AWS_BUCKET_NAME}/{s3_key}"
    return file_s3_url
