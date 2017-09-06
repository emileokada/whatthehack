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
    for key in ['geometry/location/lat', 'geometry/location/lng', 'revenue', 'popularity', 'hipness', 'name', 'vicinity', 'photos/photo_reference', 'age_bucket']:
        x = orig
        for k in key.split('/'):
            x = x.get(k, None)
        rtv[k] = x
    return rtv

def load_from_s3(data_loc):
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
    return [filter_data(x) for x in data]

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

def nearest_atm(slat,slng):
    lat = float(slat)
    lng = float(slng)
    atms = [{'atmAddress': 'Schweigaards gt.10','atmID': 'NOR51207','atmName': 'Vaterland, Grønland ATM','city': 'Oslo','country': 'Norway','currency': 'NOK,DKK (Døgnåpen)','latitude': 59.91168,'longitude': 10.758148,'zipCode': 190},{'atmAddress': 'Olafiagangen 5','atmID': 'NOR51132','atmName': 'Grønland ATM','city': 'Oslo','country': 'Norway','currency': 'NOK','latitude': 59.912839,'longitude': 10.759237,'zipCode': 188}]
    nearest_atm = min(atms,key=lambda atm:(lat-atm['latitude'])**2+(lng-atm['longitude'])**2)
    return nearest_atm

def lambda_handler(event=None, context=None):
    if event and 'httpMethod' in event and event['httpMethod'] == 'GET':
        logger.info(event)
        path = event.get('path', '/')
        params = event.get('queryStringParameters', {})

        if path == '/data/':
            return respond(load_from_s3(os.getenv('DATA_ON_S3')))
        elif path == '/atm':
            return respond(nearest_atm(params['lat'],params['lng']))
        return respond(None, 'Invalid path')
    else:
        return respond(None, 'Invalid method')
