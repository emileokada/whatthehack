import os
import json
import boto3
import botocore
import json
import shutil
import urllib
import urllib.parse
import logging

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def filter_data(orig):
    rtv = {}
    for key in ['geometry/location/lat', 'geometry/location/lng', 'rating', 'name', 'vicinity']:
        x = orig
        for k in key.split('/'):
            x = x.get(k, None)
        rtv[k] = x
    return rtv

def lambda_handler(event=None, context=None):
    if 'httpMethod' in event and event['httpMethod'] == 'GET':
        data_loc = os.getenv('DATA_ON_S3')
        parsed_loc = urllib.parse.urlparse(data_loc)
        filename = os.path.basename(parsed_loc.path)
        local_path = os.path.join('/tmp', filename)
        if not os.path.exists(local_path):
            if parsed_loc.scheme == 's3':
                print('Copying from S3')
                session = boto3.session.Session()
                config = botocore.client.Config(signature_version='s3v4')
                s3 = session.client('s3', config=config)
                s3.download_file(parsed_loc.netloc, parsed_loc.path[1:], local_path)
            else:
                shutil.copyfile(data_loc, local_path)
        with open(local_path, 'r') as fd:
            data = json.load(fd)
        body = [filter_data(x) for x in data]
        return {'body': body, 'statusCode': 200}
    else:
        return {'statusCode': 400}
