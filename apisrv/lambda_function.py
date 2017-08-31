import os
import json
import boto3

def lambda_handler(event, context):
    print(event)
    if event['httpMethod'] == 'GET':
        return {'body': 'Hello world!'}
    elif event['httpMethod'] == 'POST':
        try:
            body = json.loads(event['body'])
        except:
            return {'statusCode': 400, 'body': 'malformed json input'}
        if 'vote' not in body:
            return {'statusCode': 400, 'body': 'missing vote in request body'}
        if body['vote'] not in ['spaces', 'tabs']:
            return {'statusCode': 400, 'body': 'vote value must be \'spaces\' or \'tabs\''}

        resp = votes_table.update_item(
            Key={'id': body['vote']},
            UpdateExpression='ADD votes :incr',
            ExpressionAttributeValues={':incr': 1},
            ReturnValues='ALL_NEW'
        )
        return {'body': '{} now has {} votes'.format(body['vote'], resp['Attributes']['votes'])}
