from dotenv import load_dotenv
from boto3 import client
import os
# import
from pprint import pprint as pp
load_dotenv('../.env')

def put():
    key_id = os.environ.get('AWS_ACCESS_KEY_ID')
    access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
    region_name = os.environ.get('AWS_DEFAULT_REGION')
    bucket = os.environ.get('AWS_BUCKET_NAME')
    c = client('s3', region_name=region_name, aws_access_key_id=key_id, aws_secret_access_key=access_key)
    f = open('../.gitignore', 'rb')
    v = c.put_object(Bucket=bucket, Key='gitignore', Body=f)
    print(type(v['ResponseMetadata']['HTTPStatusCode']))
    pp(v)

put()