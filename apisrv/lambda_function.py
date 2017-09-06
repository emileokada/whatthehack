import json
import logging
import os
import shutil
import urllib
import urllib.parse

import boto3
import botocore

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def filter_data(orig):
    rtv = {}
    for key in ['geometry/location/lat', 'geometry/location/lng', 'revenue', 'popularity', 'hipness', 'name', 'vicinity', 'photos/photo_reference', 'age_bucket']:
        x = orig
        for k in key.split('/'):
            x = x.get(k, None)
        rtv[k] = x
    return rtv

def load_from_s3(data_loc, process=True):
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
    return [filter_data(x) if process else x for x in data]

def respond(res, err=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err if err else (json.dumps(res) if res else None),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'isBase64Encoded': False
    }

def nearest_atm(fileloc, slat, slng):
    lat = float(slat)
    lng = float(slng)
    atms = load_from_s3(fileloc, process=False)
    return min(atms, key=lambda atm: (lat-atm['latitude'])**2+(lng-atm['longitude'])**2)

def lambda_handler(event=None, context=None):
    if event and 'httpMethod' in event and event['httpMethod'] == 'GET':
        logger.info(event)
        path = event.get('path', '/')
        params = event.get('queryStringParameters', {})

        if path == '/data/':
            return respond(load_from_s3(os.getenv('DATA_ON_S3')))
        elif path == '/atm':
            return respond(nearest_atm(os.getenv('ATM_ON_S3'), params['lat'], params['lng']))
        return respond(None, 'Invalid path')
    else:
        return respond(None, 'Invalid method')
