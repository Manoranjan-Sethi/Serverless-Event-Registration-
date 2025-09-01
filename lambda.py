import uuid
import boto3
import json


def lambda_handler(event, context):
    # Handle CORS preflight request
    if event.get('httpMethod') == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                'Access-Control-Allow-Methods': 'GET,POST,OPTIONS'
            },
            'body': ''
        }
    
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('eventDB')

        # Handle different event structures for API Gateway
        if event.get('body'):
            if isinstance(event['body'], str):
                body = json.loads(event['body'])
            else:
                body = event['body']
            
            event_id = str(uuid.uuid4())
            name = body.get('Name')
            age = body.get('Age') 
            email = body.get('Email')
            event_name = body.get('EventName')
        else:
            # Direct test format
            event_id = str(uuid.uuid4())
            name = event.get('Name')
            age = event.get('Age')
            email = event.get('Email')
            event_name = event.get('EventName')

        # Debug logging
        print(f"Event data: {event}")
        print(f"Name: {name}, Age: {age}, Email: {email}, EventName: {event_name}")

        # Validate required fields
        if not all([name, age, email, event_name]):
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': 'Missing required fields',
                    'received': {
                        'Name': name,
                        'Age': age,
                        'Email': email,
                        'EventName': event_name
                    }
                })
            }

        # Insert into DynamoDB
        table.put_item(Item={
            'eventID': event_id,
            'Name': name,
            'Age': int(age) if age else None,
            'Email': email,
            'EventName': event_name
        })

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST,OPTIONS'
            },
            'body': json.dumps({
                'message': 'Registration successful',
                'eventID': event_id
            })
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST,OPTIONS'
            },
            'body': json.dumps({'error': f'Internal server error: {str(e)}'})
        }